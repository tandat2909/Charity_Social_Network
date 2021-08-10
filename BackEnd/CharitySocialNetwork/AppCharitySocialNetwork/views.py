import rest_framework.exceptions
from django.contrib.auth import authenticate, login, logout, decorators
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from requests import request
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import *
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import *
from .models import *
from .paginators import PostPagePagination
from .permission import *
from .serializers import *
from rest_framework import viewsets, views, generics, permissions, status


class Index(View):
    def get(self, request):
        return HttpResponse('Chào mừng bạn tới API Từ Thiện')


class Login(View):

    def get(self, request):
        return render(request, template_name='login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        print('before login: username: ' + username, 'password: ' + password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_to = request.GET.get("next")
            if next_to is not None:
                return redirect(next_to)
            return redirect('/')
        return redirect('/accounts/login')


def logouts(request):
    logout(request)
    return redirect("/accounts/login")


class BaseViewAPI:
    list_action_upload_file = []

    def is_view_user_login(self, request, pk):
        """
               return True when request pk is user login current and else
         """
        return bool(str(request.user.id) == pk)

    def delete_custom(self, request=None, instance=None, *args, **kwargs):
        instance = instance or self.get_object()
        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_parsers(self):
        """
            Mặc định dùng JSONParser class
            Nếu action hiện tại có trong list_action_upload_file thì chuyển đổi parser mặc định sang MultiPartParser class
        :return: List instance class Parser
        """
        try:
            if self.action in self.list_action_upload_file:
                return [MultiPartParser(), ]
            return super().get_parsers()
        except:
            return super().get_parsers()


class UserView(BaseViewAPI, GenericViewSet, CreateModelMixin, UpdateModelMixin):
    '''
        Tất cả action API dành cho User
        url: /api/accounts/

        todo: chưa validate các trường phonenumber,avatar,birthday,gender

    '''

    queryset = User.objects.exclude(Q(is_superuser=True) | Q(is_active=False))

    list_action_upload_file = ["create", ]

    def get_serializer_class(self):
        '''
            action change_password: dùng UserChangePasswordSerializer class
            action register(create): dùng UserRegisterSerializer class
            action get, update info: dùng UserSerializer class
        :return: serializer class
        '''
        if self.action == "change_password":
            return UserChangePasswordSerializer
        if self.action == 'create':
            return UserRegisterSerializer
        return UserSerializer

    # def create(self, request, *args, **kwargs):
    #     print(request.__dict__)
    #     file = request.FILES.get("avatar")
    #     file_name = str(file)
    #     with default_storage.open('images/' + file_name, 'wb+') as destination:
    #         for chunk in file.chunks():
    #             destination.write(chunk)
    #         print(destination.path)
    #     return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'change_password']:
            return [PermissionUserChange(), ]
        if self.action == "create":
            return [permissions.AllowAny(), ]

        return [PermissionUserViewInfo(), ]

    def update(self, request, *args, **kwargs):
        if self.is_view_user_login(request, kwargs.get("pk")):
            return super().update(request, *args, **kwargs)
        raise PermissionDenied()

    @action(methods=["PATCH"], detail=False, url_path='change_password', name="change_password")
    def change_password(self, request, **kwargs):

        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, request.data)
        logout(request)
        request.auth.revoke()
        return Response(data={'success': 'Change password success'}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="logout", name="logout")
    def logout(self, request, *args, **kwargs):
        logout(request)
        if request.auth:
            request.auth.revoke()
        return Response(status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="profile", name="profile")
    def profile(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            pk = kwargs.get("id")
            return Response(UserSerializer(self.queryset.get(pk=pk)).data, status.HTTP_200_OK)
        return Response(UserSerializer(request.user).data, status.HTTP_200_OK)


class EmotionViewBase:

    def statistical_emotion_post(self, post_id, **kwargs):
        """
        Thống kê tất cả biểu cảm bài viết
        tất cả các fields của EmotionType và thêm một fields amount
        amount: tổng số lượng mỗi loại biểu cảm mà bài viết có
        các loại biểu cảm không có sẽ không được thêm vào
        :param post_id:
        :return:
        """
        data = EmotionType.objects.all() \
            .filter(emotionpost__post=post_id, emotionpost__active=True) \
            .annotate(amount=Count('id'))
        return data

    def detail_emotions_post(self, post_id, **kwargs):
        """
        Lấy tất cả emotions post của bài viết theo id bài viết

        :param post_id: id bài viết
        :return: QuerySet<[<EmotionPost: Like>, <EmotionPost: Sad>]>
        """

        instances = EmotionPost.objects.filter(active=True, post=post_id)
        return instances

    def get_serializer_statistical_emotion_post(self, post_id, **kwargs):
        request = kwargs.get("request", None)
        return EmotionTypeSerializer(self.statistical_emotion_post(post_id), many=True, context={
            'request': request or self.request
        })

    def get_serializer_detail_emotions_post(self, post_id, **kwargs):
        """
        Trả về đối tượng EmotionPostSerializer
        :param post_id:
        :param kwargs:
        :return:
        """
        return EmotionPostSerializer(self.detail_emotions_post(post_id, **kwargs), many=True)

    def create_or_update_emotion(self, data, **kwargs):
        emotion_type = data.pop("emotion_type_id")
        assert EmotionType.objects.get(id=emotion_type)
        instance = None
        try:
            instance = EmotionPost.objects.get(**data)
            instance.emotion_type_id = emotion_type
            instance.save()
        except EmotionPost.DoesNotExist:
            instance = EmotionPost.objects.create(**data, emotion_type_id=emotion_type)

        return instance


class PostViewSet(BaseViewAPI, ModelViewSet, EmotionViewBase):
    queryset = NewsPost.objects.filter(active=True)
    # serializer_class = PostSerializer
    # lookup_field = {'pk', 'user_id', "user_name", "title"}
    # lookup_url_kwarg = "user"
    list_action_upload_file = ["create", 'update', 'partial_update', 'create_report']
    pagination_class = PostPagePagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = [
        'category',
        'hashtag',
        'user',
        'created_date'
    ]
    ordering_fields = [
        "id",
        "user",
        "category",
        "hashtag",
        "description",
        "created_date",
        "title"
    ]
    search_fields = [
        # tìm kiếm theo thứ tự từ trên xuống
        'title',
        'description',
        'hashtag__name',
        'content',
        'category__name',
    ]

    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'get_comments', 'get_emotion_post']:
            return [permissions.AllowAny(), ]
        if self.action in ["is_post_allowed", "get_list_pending_post"]:
            return [OR(PermissionUserMod(), IsAdminUser()), ]
        return [permissions.IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.action in ['list', ]:
            return PostListSerializer
        if self.action in ['create_or_update_or_delete_emotion_post', ]:
            return EmotionPostSerializer
        if self.action in ["create", 'update', 'partial_update']:
            return PostCreateSerializer
        if self.action.__eq__("is_post_allowed"):
            return PostChangeFieldIsShow
        if self.action in ['get_comments', ]:
            return CommentSerializer
        if self.action in ['create_comment', ]:
            return CommentCreateSerializer
        if self.action in ["create_report", ]:
            return ReportPostCreateSerializer
        if self.action in ['set_auctioneer_winning', 'offer_item']:
            return None
        return PostSerializer

    def list(self, request, *args, **kwargs):
        """
        <pre>
            Mặc định lấy 30 bài viết mới nhất và được mod duyệt cho tất cả người dùng
            <b>Filter:</b>
                Lọc dữ liệu được chỉ định
               <b>Params: </b>
                    + user = True: lấy tất cả bài viết của user hiện tại bao gồm bài chưa được mod duyệt và đã duyệt theo thời gian giảm dần
                    + category = <category_id>: trả về list bài viết theo danh mục (loại bài viết)
                    + hashtag = <nội dung>: trả về list bài viết có nội dung hashtag cần tìm
                    + created_date: trả về list bài viết từ ngày <data_from> đến <date_to>
                Ví dụ: ví dụ: http://localhost:8000/api/newspost/?category=1&hashtag=1&hashtag=2
                    => trả ra kết quả các bài viết thuộc danh mục có id là 1 và các bài viết có hashtag id 1 hoặc 2
               <b>Lưu ý:</b>
                    Các fields <b>user,category,hashtag</b> là id yêu cầu <b>kiểu dữ liệu</b> là <b>số nguyên</b>
            <b>Ordering:</b>
                Chỉ định các trường sắp xếp theo thứ tự tăng dần hoặc giản dần
                Các tham số chỉ định sắp xếp
                <b>Params:</b>
                    + <b>id:</b> sắp xếp theo id bài viết
                    + <b>user:</b> sắp xếp theo id user
                    + <b>category:</b> sắp xếp theo category_id
                    + <b>hashtag:</b> sắp xếp theo hashtag_id
                    + <b>description:</b> sắp xếp theo chữ cái đầu description
                    + <b>created_date:</b> sắp xếp theo ngày tạo bài viết
                    + <b>title:</b> sắp xếp theo chữ cái đầu của tiêu đề
                Ví dụ: http://localhost:8000/api/newspost/?ordering=id
                    => trả về kết quả được sắp xếp theo id bài viết tăng dần
                <b>Lưu ý:</b>
                    Để chọn chế độ sắp xếp giảm dần ta thêm dấu '-' trước tên field được chỉ định
                       + ví dụ: http://localhost:8000/api/newspost/?ordering=-category
                       => url trên trả kết quả sắp xếp giảm dần theo category_id
            <b>Search:</b>
                Tìm kiếm tất cả bài viết có nội dung liên quan trên các trường được cấu hình sẵn
                <b>Fields:</b> ['title','description','hashtag__name','content','category__name']
                <b>Param:</b>
                    + <b>search</b>: gán nội dung cần tìm kiếm
                Ví dụ: http://localhost:8000/api/newspost/?search=trẻ+em
                    trả về tất cả bài viết có nội dung liên quan
        </pre>
        """
        # print(request.query_params)
        queryset = self.filter_queryset(self.get_queryset().filter(is_show=True))
        # print(queryset.query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        # xóa bài viết của chính user đó nếu khác thì không đc
        instance = self.get_object()
        if instance.user_id == request.user.id:
            return self.delete_custom(request, *args, **kwargs)
        raise PermissionDenied()

    def create(self, request, *args, **kwargs):
        '''
            price_start: tạo bài viết đấu giá
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(**{"user": request.user})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.user.id:
            return super().update(request, *args, **kwargs)
        raise PermissionDenied()

    @action(methods=["PATCH"], detail=True, url_path="is-post-allowed")
    def is_post_allowed(self, request, pk, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        instance.is_show = serializer.data["is_show"]
        instance.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="user")
    def get_post_by_user(self, request, *args, **kwargs):
        '''
            Trả về tất cả bài viết của user đang đăng nhập bao gồm các bài chưa duyệt của user

        '''
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user.id))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, url_path="list_pending_post")
    def get_list_pending_post(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(is_show=False))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # comment

    @action(methods=["GET"], detail=True, url_path="comments")
    def get_comments(self, request, pk, **kwargs):
        '''
            mặc định lấy 30 comment đầu tiên
        '''
        try:
            # comment_parent = request.query_params.get("comment", None)
            # lấy tất cả comment không có comment_parent
            queryset = self.get_object().comments.filter(active=True)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=True, url_path="comment")
    def create_comment(self, request, pk, **kwargs):
        """
            tạo comment bài viết
            <b>Param</b>
                có 2 tham số:
                + content: nội dung content
                + comment_parent: <comment_id>
                lưu ý: Nếu không để tham số comment_parent mặc định tạo comment cho bài viết ngược lại nếu có sẽ tạo comment con cho comment
        """
        comment_parent = request.data.pop("comment_parent", None)
        serializer_comment = CommentCreateSerializer(data=request.data)
        serializer_comment.is_valid(raise_exception=True)
        instance_comment = serializer_comment.save(**{"user": request.user})
        instance_comment_parent = instance_comment
        try:
            if comment_parent:
                instance_comment_parent = self.get_object().comments.get(id=comment_parent)
                instance_comment_parent.comment_child.add(instance_comment)
                instance_comment_parent.save()
            else:
                self.get_object().comments.add(instance_comment)
                self.get_object().save()
            return Response(data=CommentSerializer(instance_comment_parent).data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            raise rest_framework.exceptions.NotFound({"detail": "comment_parent not exist"})

    # end comment

    # emotion

    @action(methods=["GET"], detail=True, )
    def get_emotion_post(self, request, pk, **kwargs):
        post_id = self.get_object().id
        serializer_statistical = self.get_serializer_statistical_emotion_post(post_id)
        serializer_emotion_post = self.get_serializer_detail_emotions_post(post_id)
        return Response(data={
            'statistical': serializer_statistical.data,
            'data': serializer_emotion_post.data
        }, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True, url_path='emotions', name="emotions")
    def create_or_update_or_delete_emotion_post(self, request, pk, **kwargs):
        """
        <pre>
            <b>Chức năng:</b>
                + add: Thêm biểu cảm cho bài viết
                + update: Thay đổi loại biểu cảm
                + delete: Xóa biểu cảm của user với bài viết
            <b>Param:</b>
                + emotion_type: <id> chỉ định loại biểu cảm, Kiểu dữ liệu <b>số nguyên</b>
                + action: [delete,] chỉ định tham số này để thực hiện <b>delete</b> biểu cảm
            <b>Ví dụ:</b>
                + action add: http://localhost:8000/api/newspost/6/emotions/?emotion_type=3
                => thêm hoặc update biểu cảm mới
                + action delete:http://localhost:8000/api/newspost/6/emotions/?action=delete
                => delete biểu cảm user dành cho bài viết
                    response: status code 204
        </pre>
        """
        if request.query_params.get("action", '').__eq__('delete'):
            ins = EmotionPost.objects.get(author_id=request.user.id, post_id=self.get_object().id).delete()
            print(ins)
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'author_id': request.user.id or None,
            'post_id': self.get_object().id or None,
            'emotion_type_id': request.query_params.get("emotion_type", None),
        }
        try:
            instance_emotion = super().create_or_update_emotion(data)
            return Response(data=EmotionPostSerializer(instance_emotion).data, status=status.HTTP_200_OK)
        except EmotionType.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Emotion type not exist")

    # end emtion

    # Report
    @action(methods=["POST"], detail=True, url_path="report")
    def create_report(self, request, pk, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(**{"post": self.get_object(), "user": request.user})
        return Response(ReportPostSerializer(instance, context={"request": request}).data, status=status.HTTP_200_OK)

    @action(methods=["PATCH"], detail=True)
    def set_auctioneer_winning(self, request, pk, **kwargs):
        """
        <pre>
            Chọn người đấu giá chiến thắng cho phiên đấu giá
            <b>request params:</b>
                +id: post_id:int id bài viết
            <b>Body:</b>
                + history_auction: history_auction_id:int id lịch sử người đấu giá
        </pre>
        """

        if request.user.id is not self.get_object().user.id:
            raise PermissionDenied()
        try:

            history_auction_id = request.data.get("history_auction", None)
            if history_auction_id is None or type(history_auction_id) is not int:
                raise rest_framework.exceptions.ValidationError(
                    "Require history_auction_id not none and Require history_auction_id is Integer")
            instance_history_auction = HistoryAuction.objects.get(pk=history_auction_id)
            instance_auction_item = AuctionItem.objects.get(post=self.get_object().id)
            instance_auction_item.receiver = instance_history_auction.user
            instance_auction_item.price_received = instance_history_auction.price
            instance_history_auction.save()
            return Response(AuctionItemSerializer(instance_auction_item).data, status=status.HTTP_200_OK)
        except AuctionItem.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Bài viết không phải loại bài viết đấu giá")
        except HistoryAuction.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Lịch sử đấu giá này không tồn tại")
        except NewsPost.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Bài viết không tồn tại")

    @action(methods=["PATCH"], detail=True, url_path="offer")
    def offer_item(self, request, pk, **kwargs):
        offer = request.data.get("offer", None)
        if offer is None:
            raise rest_framework.exceptions.NotFound({"offer":"field is not empty"})
        try:
            instance_auction_item = AuctionItem.objects.get(post=self.get_object().id)
            if offer <= instance_auction_item.price_start:
                raise rest_framework.exceptions.ValidationError(
                    {"offer": "offer không hợp lệ giá phải lớn hơn hoặc bằng giá khởi điểm"})
            history_data = {
                "user": request.user.id,
                "price": offer,
                "post": self.get_object().id
            }
            serializer_history = HistoryAuctionSerializer(data=history_data)
            serializer_history.is_valid(raise_exception=True)
            serializer_history.save()
            return Response(serializer_history.data, status=status.HTTP_200_OK)
        except AuctionItem.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Bài viết không phải loại bài viết đấu giá")


# end Report


class ReportViewSet(ListModelMixin, GenericViewSet):
    queryset = OptionReport.objects.all()
    serializer_class = OptionReportSerializer
    permission_classes = [PermissionUserReport]

    # todo api cần làm
    # get list option report
    # create report post


class EmotionViewSet(ModelViewSet, EmotionViewBase):
    queryset = EmotionPost.objects.all()
    serializer_class = EmotionPostSerializer
    lookup_field = 'post_id'

    def retrieve(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id", None)
        serializer_statistical = self.get_serializer_statistical_emotion_post(post_id)
        serializer_emotion_post = self.get_serializer_detail_emotions_post(post_id)
        return Response(data={
            'statistical': serializer_statistical.data,
            'data': serializer_emotion_post.data
        }, status=status.HTTP_200_OK)

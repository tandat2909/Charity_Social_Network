import datetime
import decimal
import re
from collections import OrderedDict

import cloudinary
import rest_framework
from MySQLdb import IntegrityError
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, OR
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from ..filters import DjangoFilterBackendCustom
from ..models import NewsPost, AuctionItem, HistoryAuction, Comment, \
    EmotionPost, EmotionType, NewsCategory, User, Hashtag
from ..paginators import PostPagePagination, CommentPagePagination, ImagePagePagination
from ..permission import PermissionUserMod
from ..serializers import PostListSerializer, EmotionPostSerializer, \
    PostCreateSerializer, PostChangeFieldIsShow, CommentSerializer, CommentCreateSerializer, ReportPostCreateSerializer, \
    PostSerializer, PostDetailSerializer, ReportPostSerializer, AuctionItemSerializer, HistoryAuctionCreateSerializer, \
    CategoryPostSerializer, HashtagsSerializer, UserViewModelSerializer, HistoryAuctionSerializer, \
    AuctionItemViewSerializer, PostImageSerializer
from ..view.baseview import BaseViewAPI, EmotionViewBase


class PostViewSet(BaseViewAPI, EmotionViewBase, ModelViewSet):
    queryset = NewsPost.objects.filter(active=True)
    # serializer_class = PostSerializer
    # lookup_field = {'pk', 'user_id', "user_name", "title"}
    # lookup_url_kwarg = "user"
    list_action_upload_file = ["create", 'update', 'partial_update', 'create_report']
    # pagination_class = PostPagePagination
    filter_backends = [DjangoFilterBackendCustom, OrderingFilter, SearchFilter]
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

    def get_queryset(self):
        if self.action in ["create_comment", "get_comment", "list"]:
            return self.queryset.filter(is_show=True)
        return self.queryset

    def get_permissions(self):
        if self.action in ['list', 'get_comments', 'get_emotion_post','ckeditor_upload', 'retrieve', 'category',
                           "get_all_image_post_user"]:
            return [permissions.AllowAny(), ]
        if self.action in ["is_post_allowed", "get_list_pending_post"]:
            return [OR(PermissionUserMod(), IsAdminUser()), ]
        return [permissions.IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.action in ["retrieve", ]:
            return PostDetailSerializer
        if self.action in ['list', 'get_post_by_user']:
            return PostListSerializer
        if self.action in ['category']:
            return CategoryPostSerializer
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

    def retrieve(self, request, *args, **kwargs):

        if self.is_instance_of_user(request, self.get_object()) or request.user.is_superuser:
            return Response(self.get_serializer(self.get_object(), context={"request": request}).data,
                            status=status.HTTP_200_OK)
        if not self.get_object().is_show:
            raise rest_framework.exceptions.NotFound()
        data = self.get_serializer(self.get_object()).data.copy()
        data["historyauction"] = []
        try:
            if request.user.is_authenticated and AuctionItem.objects.filter(post=self.get_object().id).exists():
                instance_history_auction_of_user_current = HistoryAuction.objects.get(user=request.user.id,
                                                                                      post=self.get_object().id,
                                                                                      active=True)
                data["historyauction"] = [HistoryAuctionSerializer(instance_history_auction_of_user_current).data, ]
        except HistoryAuction.DoesNotExist:
            print("user không đấu giá")
        finally:
            return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        <pre>
            Mặc định lấy 30 bài viết mới nhất và được mod duyệt cho tất cả người dùng
            <b>Filter:</b>
                Lọc dữ liệu được chỉ định
               <b>Params: </b>
                    + user = <id:int>: lấy tất cả bài viết của user theo id được duyệt
                    + category = <category_id:id>: trả về list bài viết theo danh mục (loại bài viết)
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
        queryset = self.get_queryset()
        # print(queryset.query)
        self.pagination_class = PostPagePagination
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
        serializer.is_valid(raise_exception=False)
        # print(request.data,type(request.data.getlist("hashtag",None)))
        try:
            hashtag = request.data.getlist("hashtag", None)
        except:
            hashtag = request.data.get("hashtag", None)

        instance = serializer.save(**{"user": request.user, 'hashtag': hashtag})
        self.add_notification(**settings.NOTIFICATION_MESSAGE.get("add_post"))

        return Response(PostSerializer(instance, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if self.is_instance_of_user(request, self.get_object()):
            return super().update(request, *args, **kwargs)
        raise PermissionDenied()

    def perform_update(self, serializer, **kwargs):
        try:
            hashtag = self.request.data.getlist("hashtag", None)
        except:
            hashtag = self.request.data.get("hashtag", None)
        kwargs["hashtag"] = hashtag
        kwargs["is_show"] = False
        # print("update view: hashtag: ", hashtag)
        serializer.save(**kwargs)
        self.add_notification(**settings.NOTIFICATION_MESSAGE.get("update_post"))

    @action(methods=["PATCH"], detail=True, url_path="is-post-allowed")
    def is_post_allowed(self, request, pk, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        if instance.is_show and serializer.data["is_show"]:
            return Response({"error": "Bài viết đã được duyệt"}, status=status.HTTP_400_BAD_REQUEST)
        instance.is_show = serializer.data["is_show"]
        instance.save()
        if instance.is_show:
            self.add_notification(title="Duyệt bài",
                                  user=instance.user,
                                  message="Bài viết {post_title} đã được duyệt".format(post_title=instance.title)
                                  )
            if instance.category.id == 1:
                # print(Group.objects.get(name="User").user_set.all())
                for u in Group.objects.get(name="User").user_set.all():
                    # print(instance.info_auction.first(), u)
                    if u.id != instance.user.id:
                        self.add_notification(title="Sự kiện đấu giá", user=u,
                                              message="{title} diễn ra vào ngày {start} - {end}".
                                              format(
                                                  title=instance.title,
                                                  start=instance.info_auction.first().start_datetime,
                                                  end=instance.info_auction.first().end_datetime
                                              ))
        return Response(status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="user")
    def get_post_by_user(self, request, *args, **kwargs):
        '''
            Trả về tất cả bài viết của user đang đăng nhập bao gồm các bài chưa duyệt của user
            Cần đăng nhập tài khoản user
            filter:
                + có tất cả các tham số filter list post
                + thêm filter bài viết chưa duyệt hoặc đã duyệt bài của user đang đăng nhập
                    - browser = 1 : filter lấy tất cả bài viết được duyệt
                    - browser = 0 : filter lấy tất cả bài viết chưa duyệt

        '''
        browser = request.query_params.get("browser", None)
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user.id))
        if browser:
            try:
                queryset = queryset.filter(is_show=bool(int(browser)))
            except:
                pass
        self.pagination_class = PostPagePagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="list_pending_post")
    def get_list_pending_post(self, request):
        """
            Cần đăng nhập tài khoản user mod (tài khoản duyệt bài)

        """
        queryset = self.filter_queryset(self.get_queryset().filter(is_show=False))
        self.pagination_class = PostPagePagination
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
            queryset = self.get_object().comment_set.filter(active=True, comment_parent=None)
            self.pagination_class = CommentPagePagination
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
            <b>Require</b>
                + Yêu cầu đăng nhập
                + content
            API v2:
                thay đổi url
        """

        serializer_comment = CommentCreateSerializer(data={**request.data})
        serializer_comment.is_valid(raise_exception=True)
        instance_comment = serializer_comment.save(**{"user": request.user, "post": self.get_object()})
        try:
            if request.data.get("comment_parent", None) is not None:
                # print(self.get_object().user)
                # thông báo chủ chủ comment parent có comment mới
                self.add_notification(title="Bình luận mới",
                                      user=instance_comment.comment_parent.user,
                                      message=request.user.get_full_name() +
                                              " đã phản hồi bình luận của bạn về bài viết của " +
                                              self.get_object().user.get_full_name())

            # kiểm tra bài viết hiện tại có phải của user đang bình luận nếu phải sẽ không add thông báo
            if not self.is_instance_of_user(request, self.get_object()):
                self.add_notification(title="Bình luận mới",
                                      message=request.user.get_full_name() + " đã bình luận bài viết của bạn",
                                      user=self.get_object().user)
            return Response(data=CommentSerializer(instance_comment).data, status=status.HTTP_201_CREATED)
        except Comment.DoesNotExist:
            raise rest_framework.exceptions.NotFound({"detail": "comment_parent not exist"})

    # end comment

    # emotion

    @action(methods=["GET"], detail=True, )
    def get_emotion_post(self, request, pk, **kwargs):
        post_id = self.get_object().id
        serializer_statistical = self.get_serializer_statistical_emotion_post(post_id)
        serializer_emotion_post = self.get_serializer_detail_emotions_post()
        return Response(data={
            'statistical': serializer_statistical.data,
            'data': serializer_emotion_post.data
        }, status=status.HTTP_200_OK)

    @action(methods=["PATCH"], detail=True, url_path='emotions', name="emotions")
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
            EmotionPost.objects.get(user_id=request.user.id, post_id=self.get_object().id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = {
            'user_id': request.user.id or None,
            'post_id': self.get_object().id or None,
            'type_id': request.query_params.get("emotion_type", None),
        }
        try:

            instance_emotion = self.create_or_update_emotion(data, EmotionPost)
            self.add_notification(title="",
                                  message=(self.request.user.get_full_name() or self.request.user.username) +
                                          " " + instance_emotion.type.name + ' bài viết " ' + self.get_object().title + ' " của bạn"',
                                  user=self.get_object().user
                                  )
            return Response(data=EmotionPostSerializer(instance_emotion, context={"request": request}).data,
                            status=status.HTTP_200_OK)
        except EmotionType.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Emotion type not exist")

    # end emtion

    # Report
    @action(methods=["POST", ], detail=True, url_path="report")
    def create_report(self, request, pk, **kwargs):
        """
            + Chức năng:
                - Tạo report bài viết
            + Method: POST
            + Authorization: True
            + Request Body:

        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(**{"post": self.get_object(), "user": request.user})
        # todo lấy user ra thông báo cho tất cả admin không được performance
        instance_user_admin = User.objects.filter((
                                                          Q(is_superuser=True) |
                                                          Q(is_staff=True) |
                                                          Q(user_permissions__codename__contains='mod')
                                                  )
                                                  & Q(is_active=True))
        message = 'Người dùng {name} đã report \n{content}'.format(name=self.request.user.get_full_name(),
                                                                   content=instance.__str__())
        for user in instance_user_admin:
            self.add_notification(title='Report', message="Bài viết " + self.get_object().title, user=user)
            user.email_user(subject="[Charity Social Network][Report][News Post]", message=message)

        request.user.email_user(subject="[Charity Social Network][Report]",
                                message=instance.__str__()
                                        + "\n Cảm ơn bạn đã Report chúng tôi sẽ xem xét "
                                          "và gửi thông báo cho bạn sớm nhất")
        return Response(ReportPostSerializer(instance,context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

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
        # kiểm tra có phải bài viết của user không
        if not self.is_instance_of_user(request, self.get_object()):
            raise PermissionDenied()
        try:
            # kiểm tra request có gửi phiếu đấu giá lên không
            history_auction_id = request.data.get("history_auction", None)
            if history_auction_id is None or type(history_auction_id) is not int:
                raise rest_framework.exceptions.ValidationError(
                    "Require history_auction_id not none and Require history_auction_id is Integer")
            # lấy phiếu đấu giá đồng thời kiểm tra nó tồn tại không
            instance_history_auction = HistoryAuction.objects.get(pk=history_auction_id)
            # lấy phiên đấu giá đông thời kiểm tra nó có phải bài viết đấu giá không
            instance_auction_item = AuctionItem.objects.get(post=self.get_object().id)
            # pass 2 điều kiện trên gán người chiến thắng và giá người chiến thắng đưa ra
            instance_auction_item.receiver = instance_history_auction.user
            instance_auction_item.price_received = instance_history_auction.price

            instance_auction_item.save()

            self.add_notification(title="Thông báo đấu giá",
                                  message="Chúc mừng bạn là người chiến thắng trong buổi đấu giá " + self.get_object().title,
                                  user=instance_history_auction.user
                                  )
            self.add_notification(title="Thông báo thánh toán đấu giá",
                                  message=str(instance_auction_item.price_received) +
                                          'VNĐ là số tiền bạn phải thanh toán cho ban tổ chức từ thiện của bài viết "' +
                                          self.get_object().title,
                                  user=instance_history_auction.user
                                  )
            instance_history_auction.user.email_user(subject="[Charity Social Network][Thông báo đấu giá]",
                                                     message="Chúc mừng bạn là người chiến thắng đấu giá"
                                                     )

            return Response(AuctionItemViewSerializer(instance_auction_item).data, status=status.HTTP_200_OK)
        except AuctionItem.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Bài viết không phải loại bài viết đấu giá")
        except HistoryAuction.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Lịch sử đấu giá này không tồn tại")
        except NewsPost.DoesNotExist:
            raise rest_framework.exceptions.NotFound("Bài viết không tồn tại")

    def is_show(self):
        """
            Kiểm tra bài viết sẵn sàng hiển thị cho người dùng xem hay chưa
            nếu bài viết sãn sàng return True ngược return throw exception, kèm mã lỗi status code 404 cho client
        :return: True
        :exception rest_framework.exceptions.NotFound
        """
        if not self.get_object().is_show:
            raise rest_framework.exceptions.NotFound({"error": "Bài viết đang chờ được duyệt"})
        return True

    @action(methods=["PATCH"], detail=True, url_path="offer")
    def offer_item(self, request, pk, **kwargs):
        self.is_show()
        return self.offer(request, post=self.get_object())

    @action(methods=["DELETE"], url_path="hashtag/(?P<hash_tag_id>[a-z0-9]+)/delete", detail=True)
    def delete_hashtag(self, request, pk, hash_tag_id, **kwargs):
        try:
            if self.is_instance_of_user(request, self.get_object()):
                # print(hash_tag_id, pk, kwargs)
                instance_post = self.get_object()
                instance_post.hashtag.get(pk=hash_tag_id).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            raise rest_framework.exceptions.PermissionDenied()
        except ValueError as ex:
            return Response({"error": ex.__str__()}, status=status.HTTP_400_BAD_REQUEST)
        except Hashtag.DoesNotExist:
            return Response({"error": "Bài viết không có hash tag này"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["GET"], detail=False, url_path="category", )
    def category(self, request):
        instances = NewsCategory.objects.filter(active=True)
        serializer = CategoryPostSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, url_path="ckeditor/upload")
    def ckeditor_upload(self, request, **kwargs):
        try:
            uploaded_file = request.FILES["upload"]
            file = cloudinary.uploader.upload(uploaded_file)
            # print("sssssss",file.get("secure_url",None))
            filename = file.get("public_id")
            url = file.get("secure_url")
            retdata = {"url": url, "uploaded": "1", "fileName": filename}
            return Response(retdata, status=status.HTTP_200_OK)
        except:
            return Response({'error': "Lỗi upload file"}, status=400)

    @action(methods=["GET"], detail=False, url_path="get-all-image-post-user/(?P<user_id>[0-9]+)")
    def get_all_image_post_user(self, request, user_id, **kwargs):
        """
            Lấy tất cả hình ảnh theo người dùng mà bài viết đó được duyệt

        """
        query_set = self.get_queryset().filter(user=user_id, is_show=True, image__isnull=False).order_by(
            "-created_date")
        # print(query_set.query)
        self.pagination_class = ImagePagePagination
        return self.get_paginated_response(PostImageSerializer(self.paginate_queryset(query_set), many=True).data, )

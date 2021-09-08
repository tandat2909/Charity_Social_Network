import os

import cloudinary
import rest_framework.exceptions
from ckeditor_uploader.views import ImageUploadView, get_upload_filename
from ckeditor_uploader import utils
from ckeditor_uploader.backends import registry
from ckeditor_uploader.utils import storage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect
from django.utils.html import escape

from django.views import View

from oauth2_provider.models import Application
from .view import *


class Index(View):
    def get(self, request):
        o = Application.objects.get(pk=1)

        return render(request, template_name="index.html", context={"oauth2": o})


class Login(View):
    def get(self, request):
        return render(request, template_name='login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        # print('before login: username: ' + username, 'password: ' + password)
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

#
# class CKEditorUploadCloud(View):
#
#     def post(self, request, **kwargs):
#         try:
#             if request.user.is_authenticated:
#                 uploaded_file = request.FILES["upload"]
#                 file = cloudinary.uploader.upload(uploaded_file)
#                 # print("sssssss",file.get("secure_url",None))
#                 filename = file.get("public_id")
#                 url = file.get("secure_url")
#                 retdata = {"url": url, "uploaded": "1", "fileName": filename}
#                 return JsonResponse(retdata)
#             raise rest_framework.exceptions.PermissionDenied()
#         except:
#             return JsonResponse({'error': "Lỗi upload file"}, status=400)
#
# #
# class BaseViewAPI:
#     list_action_upload_file = []
#
#     def is_view_user_login(self, request, pk):
#         """
#                return True when request pk is user login current and else
#          """
#         return bool(str(request.user.id) == pk)
#
#     def is_instance_of_user(self, request, instance=None):
#         instance = instance or self.get_object()
#         try:
#             return bool(request.user.is_authenticated and request.user.id == instance.user.id)
#         except:
#             return False
#
#     def add_notification(self, title, message, user=None, request=None, *args, **kwargs):
#         """
#             user là instance User được thêm thông báo mặc dịnh sẽ lấy trong request.user
#             request: mặc định sẽ lấy self.request của lớp ViewSet
#             title: tiêu đề thông báo
#             message: nội dung thông báo
#             Nếu user và request không lấy được đồng nghĩa với việc không thêm được thông báo và hàm trả về False
#             Nếu add thành công sẽ trả về True
#
#         :param title:
#         :param message:
#         :param user:
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         try:
#             user = user or request.user or self.request.user
#             n = Notification(title=title, message=message)
#             n.save()
#             user.notifications.add(n)
#             return True
#         except Exception as ex:
#             print(ex)
#             return False
#
#     def delete_custom(self, request=None, instance=None, *args, **kwargs):
#         instance = instance or self.get_object()
#         instance.active = False
#         instance.save()
#         # add thong báo
#         if isinstance(instance, NewsPost):
#             self.add_notification(title="Xóa bài viết", message='Bạn vừa xóa bài viết "' + instance.title + '"')
#
#         if isinstance(instance, Comment):
#             self.add_notification(title="Xóa commment bài viết",
#                                   message='Bạn vừa xóa comment "' + instance.content + '"')
#
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def get_parsers(self):
#         """
#             Mặc định dùng JSONParser class
#             Nếu action hiện tại có trong list_action_upload_file thì chuyển đổi parser mặc định sang MultiPartParser class
#         :return: List instance class Parser
#         """
#         try:
#             if self.action in self.list_action_upload_file:
#                 return [MultiPartParser(), ]
#             return super().get_parsers()
#         except:
#             return super().get_parsers()
#
#     def is_between_time(self, start, end, intime=datetime.datetime.now(pytz.utc)):
#         # print(start, end, intime)
#
#         if start <= intime <= end:
#             return True
#         elif start > end:
#             end_day = datetime.time(hour=23, minute=59, second=59, microsecond=999999)
#             if start <= intime <= end_day:
#                 return True
#             elif intime <= end:
#                 return True
#         return False
#
#
# class UserView(BaseViewAPI, CreateModelMixin, UpdateModelMixin, GenericViewSet):
#     '''
#         Tất cả action API dành cho User
#         url: /api/accounts/
#
#         todo: chưa validate các trường phonenumber,avatar,birthday,gender
#
#     '''
#
#     queryset = User.objects.exclude(Q(is_superuser=True) | Q(is_active=False))
#
#     list_action_upload_file = ["create", ]
#
#     def get_serializer_class(self):
#         '''
#             action change_password: dùng UserChangePasswordSerializer class
#             action register(create): dùng UserRegisterSerializer class
#             action get, update info: dùng UserSerializer class
#         :return: serializer class
#         '''
#         if self.action == "change_password":
#             return UserChangePasswordSerializer
#         if self.action == 'create':
#             return UserRegisterSerializer
#         if self.action in ['create_report', ]:
#             return ReportUserCreateSerializer
#         if self.action in ["notification", ]:
#             return NotificationSerializer
#         return UserSerializer
#
#     # def create(self, request, *args, **kwargs):
#     #     print(request.__dict__)
#     #     file = request.FILES.get("avatar")
#     #     file_name = str(file)
#     #     with default_storage.open('images/' + file_name, 'wb+') as destination:
#     #         for chunk in file.chunks():
#     #             destination.write(chunk)
#     #         print(destination.path)
#     #     return super().create(request, *args, **kwargs)
#
#     def get_permissions(self):
#         if self.action in ['update', 'partial_update', 'change_password', ]:
#             return [PermissionUserChange(), ]
#         if self.action in ["create", "logout", 'notification_hidden']:
#             return [permissions.AllowAny(), ]
#
#         return [PermissionUserViewInfo(), ]
#
#     def update(self, request, *args, **kwargs):
#         if self.is_view_user_login(request, kwargs.get("pk")):
#             return super().update(request, *args, **kwargs)
#         raise PermissionDenied()
#
#     @action(methods=["PATCH"], detail=False, url_path='change_password', name="change_password")
#     def change_password(self, request, **kwargs):
#
#         serializer = UserChangePasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.update(request.user, request.data)
#         logout(request)
#         request.auth.revoke()
#         return Response(data={'success': 'Change password success'}, status=status.HTTP_200_OK)
#
#     @action(methods=["GET"], detail=False, url_path="logout", name="logout")
#     def logout(self, request, *args, **kwargs):
#         logout(request)
#         if request.auth:
#             request.auth.revoke()
#         return Response(status=status.HTTP_200_OK)
#
#     # @method_decorator(cache_page(60 * 60 * 2))
#     # @method_decorator(vary_on_headers("Authorization", ))
#     @action(methods=["GET"], detail=False, url_path="profile", name="profile")
#     def profile(self, request, *args, **kwargs):
#         if request.user.is_superuser or request.user.is_staff:
#             pk = kwargs.get("id")
#             return Response(UserSerializer(self.queryset.get(pk=pk)).data, status.HTTP_200_OK)
#         return Response(UserSerializer(request.user, context={
#             'request': request
#         }).data, status.HTTP_200_OK)
#
#     @action(methods=["POST"], detail=False, url_path="report")
#     def create_report(self, request, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         if serializer.validated_data.get("user_report").id == request.user.id:
#             raise rest_framework.exceptions.ValidationError({"Error": "Bạn không thể report chính bạn"})
#         instance = serializer.save(**{"user": request.user})
#         return Response(ReportUserSerializer(instance, context={"request": request}).data,
#                         status=status.HTTP_200_OK)
#
#     @action(methods=["GET", 'DELETE'], detail=False)
#     def notification(self, request, **kwargs):
#         if request.method == 'DELETE':
#             try:
#                 instance = request.user.notifications.get(pk=request.query_params.get('id'))
#                 return self.delete_custom(request, instance)
#             except Notification.DoesNotExist:
#                 raise rest_framework.exceptions.NotFound({"notification": "Id notification not Exist"})
#             except ValueError:
#                 raise rest_framework.exceptions.ValidationError(
#                     {"error": "Yêu cầu có tham số id và tham số kiểu dữ liệu là Int"})
#         queryset = request.user.notifications.filter(active=True)
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class EmotionViewBase:
#
#     def statistical_emotion_post(self, post_id, **kwargs):
#         """
#         Thống kê tất cả biểu cảm bài viết
#         tất cả các fields của EmotionType và thêm một fields amount
#         amount: tổng số lượng mỗi loại biểu cảm mà bài viết có
#         các loại biểu cảm không có sẽ không được thêm vào
#         :param post_id:
#         :return:
#         """
#         data = EmotionType.objects.all() \
#             .filter(emotionpost__post=post_id, emotionpost__active=True) \
#             .annotate(amount=Count('id'))
#         return data
#
#     def detail_emotions_post(self, post_id, **kwargs):
#         """
#         Lấy tất cả emotions post của bài viết theo id bài viết
#
#         :param post_id: id bài viết
#         :return: QuerySet<[<EmotionPost: Like>, <EmotionPost: Sad>]>
#         """
#
#         instances = EmotionPost.objects.filter(active=True, post=post_id)
#         return instances
#
#     def get_serializer_statistical_emotion_post(self, post_id, **kwargs):
#         request = kwargs.get("request", None)
#         return EmotionStatisticalSerializer(self.statistical_emotion_post(post_id), many=True, context={
#             'request': request or self.request
#         })
#
#     def get_serializer_detail_emotions_post(self, post_id, **kwargs):
#         """
#         Trả về đối tượng EmotionPostSerializer
#         :param post_id:
#         :param kwargs:
#         :return:
#         """
#
#         return EmotionPostSerializer(self.detail_emotions_post(post_id, **kwargs), many=True,
#                                      context={"request": self.request})
#
#     def create_or_update_emotion(self, data, models, **kwargs):
#         '''
#             lấy emotion type id ra kiểm tra nó có tồn tại không
#             - lấy thông tin emotion post ra nếu có thì cập nhật lại cái type mới nếu không có tạo mới
#         :param data:
#         :param kwargs:
#         :return:
#         '''
#         emotion_type = data.pop("emotion_type_id")
#         assert EmotionType.objects.get(id=emotion_type)
#         instance = None
#         try:
#             instance = models.objects.get(**data)
#             instance.emotion_type_id = emotion_type
#             instance.save()
#         except models.DoesNotExist:
#             instance = models.objects.create(**data, emotion_type_id=emotion_type)
#             self.get_object().emotions.add(instance)
#
#         return instance
#
#
# class CategoryPostViewSet(ListModelMixin, GenericViewSet):
#     queryset = NewsCategory.objects.filter(active=True)
#     serializer_class = CategoryPostSerializer
#     permission_classes = [permissions.AllowAny, ]
#
#
# class PostViewSet(BaseViewAPI, EmotionViewBase, ModelViewSet):
#     queryset = NewsPost.objects.filter(active=True)
#     # serializer_class = PostSerializer
#     # lookup_field = {'pk', 'user_id', "user_name", "title"}
#     # lookup_url_kwarg = "user"
#     list_action_upload_file = ["create", 'update', 'partial_update', 'create_report']
#     pagination_class = PostPagePagination
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     filterset_fields = [
#         'category',
#         'hashtag',
#         'user',
#         'created_date'
#     ]
#     ordering_fields = [
#         "id",
#         "user",
#         "category",
#         "hashtag",
#         "description",
#         "created_date",
#         "title"
#     ]
#     search_fields = [
#         # tìm kiếm theo thứ tự từ trên xuống
#         'title',
#         'description',
#         'hashtag__name',
#         'content',
#         'category__name',
#     ]
#
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def get_permissions(self):
#         if self.action in ['list', 'get_comments', 'get_emotion_post', 'retrieve', 'category']:
#             return [permissions.AllowAny(), ]
#         if self.action in ["is_post_allowed", "get_list_pending_post"]:
#             return [OR(PermissionUserMod(), IsAdminUser()), ]
#         return [permissions.IsAuthenticated(), ]
#
#     def get_serializer_class(self):
#         # if self.action in ["retrieve", ]:
#         #     return PostDetailSerializer
#         if self.action in ['list', ]:
#             return PostListSerializer
#         if self.action in ['category']:
#             return CategoryPostSerializer
#         if self.action in ['create_or_update_or_delete_emotion_post', ]:
#             return EmotionPostSerializer
#         if self.action in ["create", 'update', 'partial_update']:
#             return PostCreateSerializer
#         if self.action.__eq__("is_post_allowed"):
#             return PostChangeFieldIsShow
#         if self.action in ['get_comments', ]:
#             return CommentSerializer
#         if self.action in ['create_comment', ]:
#             return CommentCreateSerializer
#         if self.action in ["create_report", ]:
#             return ReportPostCreateSerializer
#         if self.action in ['set_auctioneer_winning', 'offer_item']:
#             return None
#
#         return PostSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         if self.is_instance_of_user(request, self.get_object()):
#             return Response(PostDetailSerializer(self.get_object(), context={"request": request}).data,
#                             status=status.HTTP_200_OK)
#
#         data = self.get_serializer(self.get_object()).data.copy()
#         data["historyauction"] = []
#         try:
#             if request.user.is_authenticated and AuctionItem.objects.filter(post=self.get_object().id).exist():
#                 instance_history_auction_of_user_current = HistoryAuction.objects.get(user=request.user.id,
#                                                                                       post=self.get_object().id,
#                                                                                       active=True)
#                 his_auc_dic = OrderedDict()
#                 his_auc_dic["id"] = instance_history_auction_of_user_current.id
#                 his_auc_dic["price"] = instance_history_auction_of_user_current.price
#                 his_auc_dic["user"] = instance_history_auction_of_user_current.user
#                 his_auc_dic["created_date"] = instance_history_auction_of_user_current.created_date
#                 data["historyauction"] = [his_auc_dic, ]
#                 print(data)
#         except HistoryAuction.DoesNotExist:
#             print("user không đấu giá")
#         finally:
#             return Response(data, status=status.HTTP_200_OK)
#
#     def list(self, request, *args, **kwargs):
#         """
#         <pre>
#             Mặc định lấy 30 bài viết mới nhất và được mod duyệt cho tất cả người dùng
#             <b>Filter:</b>
#                 Lọc dữ liệu được chỉ định
#                <b>Params: </b>
#                     + user = True: lấy tất cả bài viết của user hiện tại bao gồm bài chưa được mod duyệt và đã duyệt theo thời gian giảm dần
#                     + category = <category_id>: trả về list bài viết theo danh mục (loại bài viết)
#                     + hashtag = <nội dung>: trả về list bài viết có nội dung hashtag cần tìm
#                     + created_date: trả về list bài viết từ ngày <data_from> đến <date_to>
#                 Ví dụ: ví dụ: http://localhost:8000/api/newspost/?category=1&hashtag=1&hashtag=2
#                     => trả ra kết quả các bài viết thuộc danh mục có id là 1 và các bài viết có hashtag id 1 hoặc 2
#                <b>Lưu ý:</b>
#                     Các fields <b>user,category,hashtag</b> là id yêu cầu <b>kiểu dữ liệu</b> là <b>số nguyên</b>
#             <b>Ordering:</b>
#                 Chỉ định các trường sắp xếp theo thứ tự tăng dần hoặc giản dần
#                 Các tham số chỉ định sắp xếp
#                 <b>Params:</b>
#                     + <b>id:</b> sắp xếp theo id bài viết
#                     + <b>user:</b> sắp xếp theo id user
#                     + <b>category:</b> sắp xếp theo category_id
#                     + <b>hashtag:</b> sắp xếp theo hashtag_id
#                     + <b>description:</b> sắp xếp theo chữ cái đầu description
#                     + <b>created_date:</b> sắp xếp theo ngày tạo bài viết
#                     + <b>title:</b> sắp xếp theo chữ cái đầu của tiêu đề
#                 Ví dụ: http://localhost:8000/api/newspost/?ordering=id
#                     => trả về kết quả được sắp xếp theo id bài viết tăng dần
#                 <b>Lưu ý:</b>
#                     Để chọn chế độ sắp xếp giảm dần ta thêm dấu '-' trước tên field được chỉ định
#                        + ví dụ: http://localhost:8000/api/newspost/?ordering=-category
#                        => url trên trả kết quả sắp xếp giảm dần theo category_id
#             <b>Search:</b>
#                 Tìm kiếm tất cả bài viết có nội dung liên quan trên các trường được cấu hình sẵn
#                 <b>Fields:</b> ['title','description','hashtag__name','content','category__name']
#                 <b>Param:</b>
#                     + <b>search</b>: gán nội dung cần tìm kiếm
#                 Ví dụ: http://localhost:8000/api/newspost/?search=trẻ+em
#                     trả về tất cả bài viết có nội dung liên quan
#         </pre>
#         """
#         # print(request.query_params)
#         queryset = self.filter_queryset(self.get_queryset().filter(is_show=True))
#         # print(queryset.query)
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def destroy(self, request, *args, **kwargs):
#         # xóa bài viết của chính user đó nếu khác thì không đc
#         instance = self.get_object()
#         if instance.user_id == request.user.id:
#             return self.delete_custom(request, *args, **kwargs)
#         raise PermissionDenied()
#
#     def create(self, request, *args, **kwargs):
#         '''
#             price_start: tạo bài viết đấu giá
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         '''
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         instance = serializer.save(**{"user": request.user})
#         self.add_notification(**settings.NOTIFICATION_MESSAGE.get("add_post",None),request=request)
#         return Response(PostSerializer(instance, context={"request": request}).data, status=status.HTTP_201_CREATED)
#
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if request.user.id == instance.user.id:
#             return super().update(request, *args, **kwargs)
#         raise PermissionDenied()
#
#     def perform_update(self, serializer):
#         serializer.save(**{"is_show": False})
#         self.add_notification(**settings.NOTIFICATION_MESSAGE.get("update_post"))
#
#     @action(methods=["PATCH"], detail=True, url_path="is-post-allowed")
#     def is_post_allowed(self, request, pk, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         instance = self.get_object()
#         instance.is_show = serializer.data["is_show"]
#         instance.save()
#         if instance.is_show:
#             self.add_notification(title="Bài viết đã được xác nhận")
#         return Response(status=status.HTTP_200_OK)
#
#     @action(methods=["GET"], detail=False, url_path="user")
#     def get_post_by_user(self, request, *args, **kwargs):
#         '''
#             Trả về tất cả bài viết của user đang đăng nhập bao gồm các bài chưa duyệt của user
#             Cần đăng nhập tài khoản user
#         '''
#         queryset = self.filter_queryset(self.get_queryset().filter(user=request.user.id))
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#     @action(methods=["GET"], detail=False, url_path="list_pending_post")
#     def get_list_pending_post(self, request):
#         """
#             Cần đăng nhập tài khoản user mod (tài khoản duyệt bài)
#
#         """
#         queryset = self.filter_queryset(self.get_queryset().filter(is_show=False))
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#     # comment
#
#     @action(methods=["GET"], detail=True, url_path="comments")
#     def get_comments(self, request, pk, **kwargs):
#         '''
#             mặc định lấy 30 comment đầu tiên
#         '''
#         try:
#             # comment_parent = request.query_params.get("comment", None)
#             # lấy tất cả comment không có comment_parent
#             queryset = self.get_object().comments.filter(active=True)
#             page = self.paginate_queryset(queryset)
#             if page is not None:
#                 serializer = self.get_serializer(page, many=True)
#                 return self.get_paginated_response(serializer.data)
#             serializer = self.get_serializer(queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Comment.DoesNotExist:
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#     @action(methods=["POST"], detail=True, url_path="comment")
#     def create_comment(self, request, pk, **kwargs):
#         """
#             tạo comment bài viết
#             <b>Param</b>
#                 có 2 tham số:
#                 + content: nội dung content
#                 + comment_parent: <comment_id>
#                 lưu ý: Nếu không để tham số comment_parent mặc định tạo comment cho bài viết ngược lại nếu có sẽ tạo comment con cho comment
#             <b>Require</b>
#                 + Yêu cầu đăng nhập
#         """
#         comment_parent = request.data.pop("comment_parent", None)
#         serializer_comment = CommentCreateSerializer(data=request.data)
#         serializer_comment.is_valid(raise_exception=True)
#         instance_comment = serializer_comment.save(**{"user": request.user})
#         instance_comment_parent = instance_comment
#         try:
#             if comment_parent:
#                 instance_comment_parent = self.get_object().comments.get(id=comment_parent)
#                 instance_comment_parent.comment_child.add(instance_comment)
#                 instance_comment_parent.save()
#                 self.add_notification(title="Bình luận mới",
#                                       user=instance_comment_parent.user,
#                                       message=request.user.get_full_name() +
#                                               " đã phản hồi bình luận của bạn về bài viết của " +
#                                               self.get_object().user.get_full_name())
#
#             else:
#                 self.get_object().comments.add(instance_comment)
#                 self.get_object().save()
#             # kiểm tra bài viết hiện tại có phải của user đang bình luận nếu phải sẽ không add thông báo
#             if not self.is_instance_of_user(request, self.get_object()):
#                 self.add_notification(title="Bình luận mới",
#                                       message=request.user.get_full_name() + " đã bình luận bài viết của bạn",
#                                       user=self.get_object().user)
#             return Response(data=CommentSerializer(instance_comment_parent).data, status=status.HTTP_200_OK)
#         except Comment.DoesNotExist:
#             raise rest_framework.exceptions.NotFound({"detail": "comment_parent not exist"})
#
#     # end comment
#
#     # emotion
#
#     @action(methods=["GET"], detail=True, )
#     def get_emotion_post(self, request, pk, **kwargs):
#         post_id = self.get_object().id
#         serializer_statistical = self.get_serializer_statistical_emotion_post(post_id)
#         serializer_emotion_post = self.get_serializer_detail_emotions_post(post_id)
#         return Response(data={
#             'statistical': serializer_statistical.data,
#             'data': serializer_emotion_post.data
#         }, status=status.HTTP_200_OK)
#
#     @action(methods=["PATCH"], detail=True, url_path='emotions', name="emotions")
#     def create_or_update_or_delete_emotion_post(self, request, pk, **kwargs):
#         """
#         <pre>
#             <b>Chức năng:</b>
#                 + add: Thêm biểu cảm cho bài viết
#                 + update: Thay đổi loại biểu cảm
#                 + delete: Xóa biểu cảm của user với bài viết
#             <b>Param:</b>
#                 + emotion_type: <id> chỉ định loại biểu cảm, Kiểu dữ liệu <b>số nguyên</b>
#                 + action: [delete,] chỉ định tham số này để thực hiện <b>delete</b> biểu cảm
#             <b>Ví dụ:</b>
#                 + action add: http://localhost:8000/api/newspost/6/emotions/?emotion_type=3
#                 => thêm hoặc update biểu cảm mới
#                 + action delete:http://localhost:8000/api/newspost/6/emotions/?action=delete
#                 => delete biểu cảm user dành cho bài viết
#                     response: status code 204
#         </pre>
#         """
#         if request.query_params.get("action", '').__eq__('delete'):
#             ins = EmotionPost.objects.get(author_id=request.user.id, post_id=self.get_object().id).delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#         data = {
#             'author_id': request.user.id or None,
#             'post_id': self.get_object().id or None,
#             'emotion_type_id': request.query_params.get("emotion_type", None),
#         }
#         try:
#
#             instance_emotion = self.create_or_update_emotion(data, EmotionPost)
#             self.add_notification(title="",
#                                   message=(self.request.user.get_full_name() or self.request.user.username) +
#                                           " " + instance_emotion.emotion_type.name + ' bài viết " ' + self.get_object().title + ' " của bạn"',
#                                   user=self.get_object().user
#                                   )
#             return Response(data=EmotionPostSerializer(instance_emotion, context={"request": request}).data,
#                             status=status.HTTP_200_OK)
#         except EmotionType.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("Emotion type not exist")
#
#     # end emtion
#
#     # Report
#     @action(methods=["POST"], detail=True, url_path="report")
#     def create_report(self, request, pk, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         instance = serializer.save(**{"post": self.get_object(), "user": request.user})
#         return Response(ReportPostSerializer(instance, context={"request": request}).data, status=status.HTTP_200_OK)
#
#     @action(methods=["PATCH"], detail=True)
#     def set_auctioneer_winning(self, request, pk, **kwargs):
#         """
#         <pre>
#             Chọn người đấu giá chiến thắng cho phiên đấu giá
#             <b>request params:</b>
#                 +id: post_id:int id bài viết
#             <b>Body:</b>
#                 + history_auction: history_auction_id:int id lịch sử người đấu giá
#         </pre>
#         """
#         # kiểm tra có phải bài viết của user không
#         if not self.is_instance_of_user(request, self.get_object()):
#             raise PermissionDenied()
#         try:
#             # kiểm tra request có gửi phiếu đấu giá lên không
#             history_auction_id = request.data.get("history_auction", None)
#             if history_auction_id is None or type(history_auction_id) is not int:
#                 raise rest_framework.exceptions.ValidationError(
#                     "Require history_auction_id not none and Require history_auction_id is Integer")
#             # lấy phiếu đấu giá đồng thời kiểm tra nó tồn tại không
#             instance_history_auction = HistoryAuction.objects.get(pk=history_auction_id)
#             # lấy phiên đấu giá đông thời kiểm tra nó có phải bài viết đấu giá không
#             instance_auction_item = AuctionItem.objects.get(post=self.get_object().id)
#             # pass 2 điều kiện trên gán người chiến thắng và giá người chiến thắng đưa ra
#             instance_auction_item.receiver = instance_history_auction.user
#             instance_auction_item.price_received = instance_history_auction.price
#
#             instance_history_auction.save()
#
#             self.add_notification(title="Thông báo đấu giá",
#                                   message="Chúc mừng bạn là người chiến thắng trong buổi đấu giá" + self.get_object().title,
#                                   user=instance_history_auction.user
#                                   )
#             self.add_notification(title="Thông báo thánh toán đấu giá",
#                                   message=str(instance_auction_item.price_received) +
#                                           'VNĐ là số tiền bạn phải thanh toán cho ban tổ chức từ thiện của bài viết "' +
#                                           self.get_object().title,
#                                   user=instance_history_auction.user
#                                   )
#
#             return Response(AuctionItemSerializer(instance_auction_item).data, status=status.HTTP_200_OK)
#         except AuctionItem.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("Bài viết không phải loại bài viết đấu giá")
#         except HistoryAuction.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("Lịch sử đấu giá này không tồn tại")
#         except NewsPost.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("Bài viết không tồn tại")
#
#     @action(methods=["PATCH"], detail=True, url_path="offer")
#     def offer_item(self, request, pk, **kwargs):
#         offer = request.data.get("offer", None)
#         if offer is None:
#             raise rest_framework.exceptions.NotFound({"offer": "field is not empty"})
#         try:
#             instance_auction_item = AuctionItem.objects.get(post=self.get_object().id)
#             if not self.is_between_time(instance_auction_item.start_datetime, instance_auction_item.end_datetime):
#                 raise rest_framework.exceptions.ValidationError({"error": "Phiên đấu giá đã kết thúc"})
#             if offer <= instance_auction_item.price_start:
#                 raise rest_framework.exceptions.ValidationError(
#                     {"offer": "offer không hợp lệ giá phải lớn hơn hoặc bằng giá khởi điểm"})
#             history_data = {
#                 "user": request.user.id,
#                 "price": offer,
#                 "post": self.get_object().id
#             }
#             serializer_history = HistoryAuctionCreateSerializer(data=history_data)
#             serializer_history.is_valid(raise_exception=True)
#             serializer_history.save()
#             self.add_notification(title="Thông báo có giá mới", user=self.get_object().user,
#                                   message='{username} đề nghị giá {price} VNĐ cho bài viết {post_title}'.format(
#                                       username=request.user.get_full_name(),
#                                       price=str(offer),
#                                       post_title=self.get_object().title))
#             return Response(serializer_history.data, status=status.HTTP_200_OK)
#         except AuctionItem.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("Bài viết không phải loại bài viết đấu giá")
#
#     @action(methods=["GET"], detail=False, url_path="category", )
#     def category(self, request):
#         instances = NewsCategory.objects.filter(active=True)
#         serializer = CategoryPostSerializer(instances, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# # end Report
#
# class ReportViewSet(ListModelMixin, GenericViewSet):
#     queryset = OptionReport.objects.all()
#     serializer_class = OptionReportSerializer
#     permission_classes = [PermissionUserReport]
#
#
# class CommentViewSet(DestroyModelMixin, RetrieveUpdateAPIView, BaseViewAPI, EmotionViewBase, GenericViewSet):
#     queryset = Comment.objects.filter(active=True)
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated, ]
#
#     # def retrieve(self, request, *args, **kwargs):
#     #     post_id = kwargs.get("post_id", None)
#     #     serializer_statistical = self.get_serializer_statistical_emotion_post(post_id)
#     #     serializer_emotion_post = self.get_serializer_detail_emotions_post(post_id)
#     #     return Response(data={
#     #         'statistical': serializer_statistical.data,
#     #         'data': serializer_emotion_post.data
#     #     }, status=status.HTTP_200_OK)
#
#     def get_permissions(self):
#         if self.action in ["retrieve", ]:
#             return [permissions.AllowAny(), ]
#         return [permissions.IsAuthenticated(), ]
#
#     def get_serializer_class(self):
#         if self.action in ["update", 'partial_update']:
#             return CommentCreateSerializer
#         return self.serializer_class
#
#     def update(self, request, *args, **kwargs):
#         if self.is_instance_of_user(request, self.get_object()):
#             super().update(request, *args, **kwargs)
#             return Response(CommentSerializer(self.get_object(), context={"request": request}).data, status.HTTP_200_OK)
#         raise permissions.exceptions.PermissionDenied()
#
#     def destroy(self, request, *args, **kwargs):
#         if self.is_instance_of_user(request):
#             return self.delete_custom(request, request)
#         raise permissions.exceptions.PermissionDenied()
#
#     @action(methods=["PATCH"], detail=True, url_path="emotions")
#     def create_or_update_or_delete_emotion_comment(self, request, pk, **kwargs):
#         if request.query_params.get("action", '').__eq__('delete'):
#             ins = EmotionComment.objects.get(author_id=request.user.id, comment_id=self.get_object().id).delete()
#
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         data = {
#             'author_id': request.user.id or None,
#             'comment_id': self.get_object().id or None,
#             'emotion_type_id': request.query_params.get("emotion_type", None),
#         }
#         try:
#             instance_emotion = self.create_or_update_emotion(data, EmotionComment)
#             return Response(data=EmotionCommentSerializer(instance_emotion, context={"request": request}).data,
#                             status=status.HTTP_200_OK)
#         except EmotionType.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("Emotion type not exist")
#
#
# class HistoryAuctionViewSet(UpdateModelMixin, DestroyModelMixin, BaseViewAPI, GenericViewSet):
#     permission_classes = [permissions.IsAuthenticated, ]
#     queryset = HistoryAuction.objects.filter(active=True)
#     serializer_class = HistoryAuctionSerializer
#
#     def update(self, request, *args, **kwargs):
#         if super().is_instance_of_user(request, self.get_object()):
#             if request.data.get("user", None):
#                 raise rest_framework.exceptions.ValidationError(
#                     {"error": "Không thể thay đổi user chỉ được thay đổi mệnh giá tiền và mô tả"})
#             price_start = self.get_object().post.info_auction.first().price_start
#             if price_start.__gt__(decimal.Decimal(request.data.get("price"))):
#                 raise rest_framework.exceptions.ValidationError({"price": "Giá không thể thấp hơn giá ban đầu"})
#             return super().update(request, *args, **kwargs)
#         raise rest_framework.exceptions.PermissionDenied()
#
#     def destroy(self, request, *args, **kwargs):
#         if super().is_instance_of_user(request, self.get_object()):
#             return super().destroy(request, *args, **kwargs)
#         raise rest_framework.exceptions.PermissionDenied()
#
#
# class EmotionTypeViewSet(ListModelMixin, GenericViewSet):
#     queryset = EmotionType.objects.filter(active=True)
#     serializer_class = EmotionTypeSerializer
#     pagination_class = None

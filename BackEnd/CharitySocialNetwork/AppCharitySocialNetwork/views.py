import os

import cloudinary
import rest_framework.exceptions
from ckeditor_uploader.views import ImageUploadView, get_upload_filename
from ckeditor_uploader import utils
from ckeditor_uploader.backends import registry
from ckeditor_uploader.utils import storage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect
from django.utils.html import escape

from django.views import View
from graphene_django.views import GraphQLView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

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

# class LoginGraphql(LoginRequiredMixin,GraphQLView):
#
#     pass

    # def dispatch(self, request, *args, **kwargs):
    #     # request.user
    #     header = self.authenticate_header(request)
    #     # u, ac = self.authenticate(request)
    #     # print(header, u, ac)
    #     print("heaer",header,request.__dict__)
    #     return super().dispatch(request, *args, **kwargs)

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
#             return JsonResponse({'error': "L???i upload file"}, status=400)
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
#             user l?? instance User ???????c th??m th??ng b??o m???c d???nh s??? l???y trong request.user
#             request: m???c ?????nh s??? l???y self.request c???a l???p ViewSet
#             title: ti??u ????? th??ng b??o
#             message: n???i dung th??ng b??o
#             N???u user v?? request kh??ng l???y ???????c ?????ng ngh??a v???i vi???c kh??ng th??m ???????c th??ng b??o v?? h??m tr??? v??? False
#             N???u add th??nh c??ng s??? tr??? v??? True
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
#         # add thong b??o
#         if isinstance(instance, NewsPost):
#             self.add_notification(title="X??a b??i vi???t", message='B???n v???a x??a b??i vi???t "' + instance.title + '"')
#
#         if isinstance(instance, Comment):
#             self.add_notification(title="X??a commment b??i vi???t",
#                                   message='B???n v???a x??a comment "' + instance.content + '"')
#
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def get_parsers(self):
#         """
#             M???c ?????nh d??ng JSONParser class
#             N???u action hi???n t???i c?? trong list_action_upload_file th?? chuy???n ?????i parser m???c ?????nh sang MultiPartParser class
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
#         T???t c??? action API d??nh cho User
#         url: /api/accounts/
#
#         todo: ch??a validate c??c tr?????ng phonenumber,avatar,birthday,gender
#
#     '''
#
#     queryset = User.objects.exclude(Q(is_superuser=True) | Q(is_active=False))
#
#     list_action_upload_file = ["create", ]
#
#     def get_serializer_class(self):
#         '''
#             action change_password: d??ng UserChangePasswordSerializer class
#             action register(create): d??ng UserRegisterSerializer class
#             action get, update info: d??ng UserSerializer class
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
#             raise rest_framework.exceptions.ValidationError({"Error": "B???n kh??ng th??? report ch??nh b???n"})
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
#                     {"error": "Y??u c???u c?? tham s??? id v?? tham s??? ki???u d??? li???u l?? Int"})
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
#         Th???ng k?? t???t c??? bi???u c???m b??i vi???t
#         t???t c??? c??c fields c???a EmotionType v?? th??m m???t fields amount
#         amount: t???ng s??? l?????ng m???i lo???i bi???u c???m m?? b??i vi???t c??
#         c??c lo???i bi???u c???m kh??ng c?? s??? kh??ng ???????c th??m v??o
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
#         L???y t???t c??? emotions post c???a b??i vi???t theo id b??i vi???t
#
#         :param post_id: id b??i vi???t
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
#         Tr??? v??? ?????i t?????ng EmotionPostSerializer
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
#             l???y emotion type id ra ki???m tra n?? c?? t???n t???i kh??ng
#             - l???y th??ng tin emotion post ra n???u c?? th?? c???p nh???t l???i c??i type m???i n???u kh??ng c?? t???o m???i
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
#         # t??m ki???m theo th??? t??? t??? tr??n xu???ng
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
#             print("user kh??ng ?????u gi??")
#         finally:
#             return Response(data, status=status.HTTP_200_OK)
#
#     def list(self, request, *args, **kwargs):
#         """
#         <pre>
#             M???c ?????nh l???y 30 b??i vi???t m???i nh???t v?? ???????c mod duy???t cho t???t c??? ng?????i d??ng
#             <b>Filter:</b>
#                 L???c d??? li???u ???????c ch??? ?????nh
#                <b>Params: </b>
#                     + user = True: l???y t???t c??? b??i vi???t c???a user hi???n t???i bao g???m b??i ch??a ???????c mod duy???t v?? ???? duy???t theo th???i gian gi???m d???n
#                     + category = <category_id>: tr??? v??? list b??i vi???t theo danh m???c (lo???i b??i vi???t)
#                     + hashtag = <n???i dung>: tr??? v??? list b??i vi???t c?? n???i dung hashtag c???n t??m
#                     + created_date: tr??? v??? list b??i vi???t t??? ng??y <data_from> ?????n <date_to>
#                 V?? d???: v?? d???: http://localhost:8000/api/newspost/?category=1&hashtag=1&hashtag=2
#                     => tr??? ra k???t qu??? c??c b??i vi???t thu???c danh m???c c?? id l?? 1 v?? c??c b??i vi???t c?? hashtag id 1 ho???c 2
#                <b>L??u ??:</b>
#                     C??c fields <b>user,category,hashtag</b> l?? id y??u c???u <b>ki???u d??? li???u</b> l?? <b>s??? nguy??n</b>
#             <b>Ordering:</b>
#                 Ch??? ?????nh c??c tr?????ng s???p x???p theo th??? t??? t??ng d???n ho???c gi???n d???n
#                 C??c tham s??? ch??? ?????nh s???p x???p
#                 <b>Params:</b>
#                     + <b>id:</b> s???p x???p theo id b??i vi???t
#                     + <b>user:</b> s???p x???p theo id user
#                     + <b>category:</b> s???p x???p theo category_id
#                     + <b>hashtag:</b> s???p x???p theo hashtag_id
#                     + <b>description:</b> s???p x???p theo ch??? c??i ?????u description
#                     + <b>created_date:</b> s???p x???p theo ng??y t???o b??i vi???t
#                     + <b>title:</b> s???p x???p theo ch??? c??i ?????u c???a ti??u ?????
#                 V?? d???: http://localhost:8000/api/newspost/?ordering=id
#                     => tr??? v??? k???t qu??? ???????c s???p x???p theo id b??i vi???t t??ng d???n
#                 <b>L??u ??:</b>
#                     ????? ch???n ch??? ????? s???p x???p gi???m d???n ta th??m d???u '-' tr?????c t??n field ???????c ch??? ?????nh
#                        + v?? d???: http://localhost:8000/api/newspost/?ordering=-category
#                        => url tr??n tr??? k???t qu??? s???p x???p gi???m d???n theo category_id
#             <b>Search:</b>
#                 T??m ki???m t???t c??? b??i vi???t c?? n???i dung li??n quan tr??n c??c tr?????ng ???????c c???u h??nh s???n
#                 <b>Fields:</b> ['title','description','hashtag__name','content','category__name']
#                 <b>Param:</b>
#                     + <b>search</b>: g??n n???i dung c???n t??m ki???m
#                 V?? d???: http://localhost:8000/api/newspost/?search=tr???+em
#                     tr??? v??? t???t c??? b??i vi???t c?? n???i dung li??n quan
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
#         # x??a b??i vi???t c???a ch??nh user ???? n???u kh??c th?? kh??ng ??c
#         instance = self.get_object()
#         if instance.user_id == request.user.id:
#             return self.delete_custom(request, *args, **kwargs)
#         raise PermissionDenied()
#
#     def create(self, request, *args, **kwargs):
#         '''
#             price_start: t???o b??i vi???t ?????u gi??
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
#             self.add_notification(title="B??i vi???t ???? ???????c x??c nh???n")
#         return Response(status=status.HTTP_200_OK)
#
#     @action(methods=["GET"], detail=False, url_path="user")
#     def get_post_by_user(self, request, *args, **kwargs):
#         '''
#             Tr??? v??? t???t c??? b??i vi???t c???a user ??ang ????ng nh???p bao g???m c??c b??i ch??a duy???t c???a user
#             C???n ????ng nh???p t??i kho???n user
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
#             C???n ????ng nh???p t??i kho???n user mod (t??i kho???n duy???t b??i)
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
#             m???c ?????nh l???y 30 comment ?????u ti??n
#         '''
#         try:
#             # comment_parent = request.query_params.get("comment", None)
#             # l???y t???t c??? comment kh??ng c?? comment_parent
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
#             t???o comment b??i vi???t
#             <b>Param</b>
#                 c?? 2 tham s???:
#                 + content: n???i dung content
#                 + comment_parent: <comment_id>
#                 l??u ??: N???u kh??ng ????? tham s??? comment_parent m???c ?????nh t???o comment cho b??i vi???t ng?????c l???i n???u c?? s??? t???o comment con cho comment
#             <b>Require</b>
#                 + Y??u c???u ????ng nh???p
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
#                 self.add_notification(title="B??nh lu???n m???i",
#                                       user=instance_comment_parent.user,
#                                       message=request.user.get_full_name() +
#                                               " ???? ph???n h???i b??nh lu???n c???a b???n v??? b??i vi???t c???a " +
#                                               self.get_object().user.get_full_name())
#
#             else:
#                 self.get_object().comments.add(instance_comment)
#                 self.get_object().save()
#             # ki???m tra b??i vi???t hi???n t???i c?? ph???i c???a user ??ang b??nh lu???n n???u ph???i s??? kh??ng add th??ng b??o
#             if not self.is_instance_of_user(request, self.get_object()):
#                 self.add_notification(title="B??nh lu???n m???i",
#                                       message=request.user.get_full_name() + " ???? b??nh lu???n b??i vi???t c???a b???n",
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
#             <b>Ch???c n??ng:</b>
#                 + add: Th??m bi???u c???m cho b??i vi???t
#                 + update: Thay ?????i lo???i bi???u c???m
#                 + delete: X??a bi???u c???m c???a user v???i b??i vi???t
#             <b>Param:</b>
#                 + emotion_type: <id> ch??? ?????nh lo???i bi???u c???m, Ki???u d??? li???u <b>s??? nguy??n</b>
#                 + action: [delete,] ch??? ?????nh tham s??? n??y ????? th???c hi???n <b>delete</b> bi???u c???m
#             <b>V?? d???:</b>
#                 + action add: http://localhost:8000/api/newspost/6/emotions/?emotion_type=3
#                 => th??m ho???c update bi???u c???m m???i
#                 + action delete:http://localhost:8000/api/newspost/6/emotions/?action=delete
#                 => delete bi???u c???m user d??nh cho b??i vi???t
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
#                                           " " + instance_emotion.emotion_type.name + ' b??i vi???t " ' + self.get_object().title + ' " c???a b???n"',
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
#             Ch???n ng?????i ?????u gi?? chi???n th???ng cho phi??n ?????u gi??
#             <b>request params:</b>
#                 +id: post_id:int id b??i vi???t
#             <b>Body:</b>
#                 + history_auction: history_auction_id:int id l???ch s??? ng?????i ?????u gi??
#         </pre>
#         """
#         # ki???m tra c?? ph???i b??i vi???t c???a user kh??ng
#         if not self.is_instance_of_user(request, self.get_object()):
#             raise PermissionDenied()
#         try:
#             # ki???m tra request c?? g???i phi???u ?????u gi?? l??n kh??ng
#             history_auction_id = request.data.get("history_auction", None)
#             if history_auction_id is None or type(history_auction_id) is not int:
#                 raise rest_framework.exceptions.ValidationError(
#                     "Require history_auction_id not none and Require history_auction_id is Integer")
#             # l???y phi???u ?????u gi?? ?????ng th???i ki???m tra n?? t???n t???i kh??ng
#             instance_history_auction = HistoryAuction.objects.get(pk=history_auction_id)
#             # l???y phi??n ?????u gi?? ????ng th???i ki???m tra n?? c?? ph???i b??i vi???t ?????u gi?? kh??ng
#             instance_auction_item = AuctionItem.objects.get(post=self.get_object().id)
#             # pass 2 ??i???u ki???n tr??n g??n ng?????i chi???n th???ng v?? gi?? ng?????i chi???n th???ng ????a ra
#             instance_auction_item.receiver = instance_history_auction.user
#             instance_auction_item.price_received = instance_history_auction.price
#
#             instance_history_auction.save()
#
#             self.add_notification(title="Th??ng b??o ?????u gi??",
#                                   message="Ch??c m???ng b???n l?? ng?????i chi???n th???ng trong bu???i ?????u gi??" + self.get_object().title,
#                                   user=instance_history_auction.user
#                                   )
#             self.add_notification(title="Th??ng b??o th??nh to??n ?????u gi??",
#                                   message=str(instance_auction_item.price_received) +
#                                           'VN?? l?? s??? ti???n b???n ph???i thanh to??n cho ban t??? ch???c t??? thi???n c???a b??i vi???t "' +
#                                           self.get_object().title,
#                                   user=instance_history_auction.user
#                                   )
#
#             return Response(AuctionItemSerializer(instance_auction_item).data, status=status.HTTP_200_OK)
#         except AuctionItem.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("B??i vi???t kh??ng ph???i lo???i b??i vi???t ?????u gi??")
#         except HistoryAuction.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("L???ch s??? ?????u gi?? n??y kh??ng t???n t???i")
#         except NewsPost.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("B??i vi???t kh??ng t???n t???i")
#
#     @action(methods=["PATCH"], detail=True, url_path="offer")
#     def offer_item(self, request, pk, **kwargs):
#         offer = request.data.get("offer", None)
#         if offer is None:
#             raise rest_framework.exceptions.NotFound({"offer": "field is not empty"})
#         try:
#             instance_auction_item = AuctionItem.objects.get(post=self.get_object().id)
#             if not self.is_between_time(instance_auction_item.start_datetime, instance_auction_item.end_datetime):
#                 raise rest_framework.exceptions.ValidationError({"error": "Phi??n ?????u gi?? ???? k???t th??c"})
#             if offer <= instance_auction_item.price_start:
#                 raise rest_framework.exceptions.ValidationError(
#                     {"offer": "offer kh??ng h???p l??? gi?? ph???i l???n h??n ho???c b???ng gi?? kh???i ??i???m"})
#             history_data = {
#                 "user": request.user.id,
#                 "price": offer,
#                 "post": self.get_object().id
#             }
#             serializer_history = HistoryAuctionCreateSerializer(data=history_data)
#             serializer_history.is_valid(raise_exception=True)
#             serializer_history.save()
#             self.add_notification(title="Th??ng b??o c?? gi?? m???i", user=self.get_object().user,
#                                   message='{username} ????? ngh??? gi?? {price} VN?? cho b??i vi???t {post_title}'.format(
#                                       username=request.user.get_full_name(),
#                                       price=str(offer),
#                                       post_title=self.get_object().title))
#             return Response(serializer_history.data, status=status.HTTP_200_OK)
#         except AuctionItem.DoesNotExist:
#             raise rest_framework.exceptions.NotFound("B??i vi???t kh??ng ph???i lo???i b??i vi???t ?????u gi??")
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
#                     {"error": "Kh??ng th??? thay ?????i user ch??? ???????c thay ?????i m???nh gi?? ti???n v?? m?? t???"})
#             price_start = self.get_object().post.info_auction.first().price_start
#             if price_start.__gt__(decimal.Decimal(request.data.get("price"))):
#                 raise rest_framework.exceptions.ValidationError({"price": "Gi?? kh??ng th??? th???p h??n gi?? ban ?????u"})
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

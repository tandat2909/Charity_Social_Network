import rest_framework
from django.contrib.auth import logout
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..models import User, Notification
from ..paginators import NotificationPagePagination
from ..permission import PermissionUserChange, PermissionUserViewInfo, PermissionUserMod
from ..serializers import UserChangePasswordSerializer, \
    ReportUserCreateSerializer, UserRegisterSerializer, NotificationSerializer, UserSerializer, ReportUserSerializer
from ..view.baseview import BaseViewAPI


class UserView(BaseViewAPI, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.exclude(Q(is_superuser=True) | Q(is_active=False))
    list_action_upload_file = ["create", 'create_report']

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
        if self.action in ['create_report', ]:
            return ReportUserCreateSerializer
        if self.action in ["notification", ]:
            return NotificationSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'change_password', ]:
            return [PermissionUserChange(), ]
        if self.action in ["create", "logout", 'notification_hidden']:
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

    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(vary_on_headers("Authorization", ))
    @action(methods=["GET"], detail=False, url_path="profile", name="profile")
    def profile(self, request, *args, **kwargs):
        # if request.user.is_superuser or request.user.is_staff:
        #     pk = kwargs.get("id")
        #     if pk:
        #         return Response(UserSerializer(self.queryset.get(pk=pk)).data, status.HTTP_200_OK)
        return Response(UserSerializer(request.user, context={
            'request': request
        }).data, status.HTTP_200_OK)

    @action(methods=["post"], detail=False, url_path="report")
    def create_report(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get("user_report").id == request.user.id:
            raise rest_framework.exceptions.ValidationError({"Error": "Bạn không thể report chính bạn"})
        instance = serializer.save(**{"user": request.user})
        request.user.email_user(subject="[Charity Social Network][Report]",
                                message=instance.__str__()
                                        + "\n Cảm ơn bạn đã Report chúng tôi sẽ xem xét và gửi thông báo cho bạn sớm nhất")

        # todo lấy user admin ra thông báo cho tất cả admin không được performance
        instance_user_admin = User.objects.filter(Q(is_superuser=True) & Q(is_active=True))
        message = 'Người dùng {name} đã report \n{content}'.format(name=request.user.get_full_name(),
                                                                    content=instance.__str__())
        for user in instance_user_admin:
            self.add_notification(title='Report User', message=instance.__str__(), user=user)
            user.email_user(subject="[Charity Social Network][Report][User]", message=message)

        return Response(ReportUserSerializer(instance, context={"request": request}).data,
                        status=status.HTTP_201_CREATED)

    @action(methods=["GET", 'DELETE', 'PATCH'], detail=False)
    def notification(self, request, **kwargs):
        """
            Methods:
                + Patch: dùng để set trạng thái đã đọc hay chưa
                + Delete: dùng để xóa thông báo
                + Get: lấy tất cả thông báo
            Param:
                + id: action patch,delete cần gắn tham số này trên url để định danh một đối tượng thông báo

        """
        if request.method == "GET":
            queryset = request.user.notifications.filter(active=True)

            self.pagination_class = NotificationPagePagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            self.pagination_class = None
            return Response(serializer.data, status=status.HTTP_200_OK)

        try:
            instance = request.user.notifications.get(pk=request.query_params.get('id'), active=True)
            if request.method == 'DELETE':
                return self.delete_custom(request, instance)
            if request.method == "PATCH":
                instance.new = False
                instance.save()
                return Response(status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            raise rest_framework.exceptions.NotFound({"notification": "Id notification not Exist"})
        except ValueError:
            raise rest_framework.exceptions.ValidationError(
                {"error": "Yêu cầu có tham số id và tham số kiểu dữ liệu là Int"})

    @action(methods=["GET"], url_path="is-user-mod", detail=False)
    def is_user_mod(self, request, **kwargs):
        '''
            + Chức năng:
                - Kiểm tra user đăng nhập hiện tại có phải là usermod hay không
            + Resquest body: None
            + Response body:
                usermod: giá trị kiểu bool. Nếu usermod = True là user hiện tại là usermod và ngược lại không phải user mod
        '''
        per = PermissionUserMod()

        return Response({"usermod": per.has_permission(request, self)}, status=status.HTTP_200_OK)

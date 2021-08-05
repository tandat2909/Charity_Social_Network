from django.contrib.auth import authenticate, login, logout
from django.core.handlers import exception
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.mixins import *
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import *
from .models import *
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

    def delete_custom(self, request, *args, **kwargs):
        instance = self.get_object()
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


class UserView(BaseViewAPI,GenericViewSet, CreateModelMixin, UpdateModelMixin ):
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


class PostAPI(BaseViewAPI,ModelViewSet ):
    queryset = NewsPost.objects.filter(active=True)
    serializer_class = PostSerializer
    # lookup_field = {'pk', 'user_id', "user_name", "title"}
    # lookup_url_kwarg = "user"
    list_action_upload_file = ["create",'update', 'partial_update' ]

    # permission_classes = [permissions.IsAuthenticated]

    # todo api cần làm cho post
    # (get list bài viết theo user,get list bài viết của user đang chờ mod xác nhận (is_show = False)) gộp lại làm filter get list bài viết cho nặc danh
    # api change show post của mod

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.AllowAny(), ]
        if self.action == "change_show":
            return [PermissionUserMod(),]
        return [permissions.AllowAny(), ]



    def get_serializer_class(self):
        if self.action in ["create", 'update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer

    def destroy(self, request, *args, **kwargs):
        # xóa bài viết của chính user đó nếu khác thì không đc
        instance = self.get_object()
        if instance.user_id == request.user.id:
            return self.delete_custom(request, *args, **kwargs)
        raise PermissionDenied()

    def create(self, request, *args, **kwargs):

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

    @action(methods=["GET"], detail=False, name='filter_field', url_path="filter-field")
    def filter_field(self, request, is_show, *args, **kwargs):
        print(request.__dict__)
        print(args)
        print(kwargs, is_show)
        return Response(data={"start": "pedding"}, status=status.HTTP_200_OK)


class ReportAPI(ListModelMixin, GenericViewSet):
    queryset = OptionReport.objects.all()
    serializer_class = OptionReportSerializer
    permission_classes = [PermissionUserReport]

    # todo api cần làm
    # get list option report
    # create report post

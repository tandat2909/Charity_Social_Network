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
from .permission import PermissionUserViewInfo, PermissionUserChange
from .serializers import *
from rest_framework import viewsets, views, generics, permissions, status


class Index(View):
    def get(self, request):
        return HttpResponse('Chào mừng bạn tới API Từ Thiện')


class PostAPI(viewsets.ModelViewSet):
    queryset = NewsPost.objects.filter(active=True, is_show=True)
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]


class OptionReportAPI(viewsets.ModelViewSet):
    queryset = OptionReport.objects.all()
    serializer_class = OptionReportSerializer
    permission_classes = [permissions.IsAuthenticated]


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


class UserView(CreateModelMixin, RetrieveUpdateAPIView, GenericViewSet):
    '''
        Tất cả action API dành cho User
        url: /api/accounts/

        todo: chưa validate các trường phonenumber,avatar,birthday,gender

    '''

    queryset = User.objects.exclude(Q(is_superuser=True) | Q(is_active=False))
    list_action_change = ['update', 'partial_update', 'change_password']
    parser_classes = [MultiPartParser, ]

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
        if self.action in self.list_action_change:
            return [PermissionUserChange(), ]
        if self.action == "create":
            return [permissions.AllowAny(), ]

        return [PermissionUserViewInfo(), ]

    def retrieve(self, request, *args, **kwargs):

        pk = kwargs.get("pk")
        if request.user.is_superuser or request.user.is_staff:
            return super().retrieve(request, *args, **kwargs)
        if not self.is_view_user_login(request, pk):
            raise PermissionDenied()
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if self.is_view_user_login(request, kwargs.get("pk")):
            return super().update(request, *args, **kwargs)
        raise PermissionDenied()

    def is_view_user_login(self, request, pk):
        """
               return True when request pk is user login current and else
         """
        return bool(str(request.user.id) == pk)

    @action(methods=["PATCH"], detail=False, url_path='change_password', name="change_password")
    def change_password(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, request.data)
        return Response(data={'success': 'Change password success'}, status=status.HTTP_200_OK)

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


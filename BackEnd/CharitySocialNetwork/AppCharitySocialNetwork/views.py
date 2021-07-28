from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import *
from .serializers import *

# Create your views here.
from rest_framework import viewsets


class Index(View):
    def get(self, request):
        return HttpResponse("<h1>Hè Lo</h1>")


class UserAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

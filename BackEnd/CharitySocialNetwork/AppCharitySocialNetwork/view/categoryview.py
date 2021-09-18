from rest_framework import permissions

from ..serializers import CategoryPostSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import ListAPIView
from ..models import NewsCategory


class CategoryPostViewSet(GenericViewSet, ListAPIView):
    queryset = NewsCategory.objects.filter(active=True)
    serializer_class = CategoryPostSerializer
    permission_classes = [permissions.AllowAny,]
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', views.UserAPI)

# from .admin import customAdminSite
urlpatterns = [
    path('', views.Index.as_view()),
    path('api/', include(router.urls)),
]

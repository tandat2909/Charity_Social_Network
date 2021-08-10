from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('accounts', views.UserView)
router.register('newspost', views.PostViewSet)
router.register('optionreport', views.ReportViewSet)
router.register('emotion',views.EmotionViewSet)


# from .admin import customAdminSite
urlpatterns = [
    path('', views.Index.as_view()),
    path('api/', include(router.urls)),
    path('accounts/login/', views.Login.as_view()),
    path('accounts/logout/', views.logouts),
]
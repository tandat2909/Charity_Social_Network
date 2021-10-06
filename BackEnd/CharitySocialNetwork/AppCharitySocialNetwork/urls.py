import debug_toolbar
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt

from . import views
from rest_framework import routers
from graphene_django.views import GraphQLView

router = routers.DefaultRouter()
router.register(r'accounts', views.UserView)
router.register(r'newspost', views.PostViewSet)
router.register(r'optionreport', views.ReportViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'historyauction', views.HistoryAuctionViewSet)
router.register(r'emotions', views.EmotionTypeViewSet)
router.register(r'auction',views.AuctionViewSet)
router.register(r'statistical',views.StatisticalViewSet)
router.register(r'category',views.CategoryPostViewSet)
router.register(r'pay',views.PayViewSet)
# from .admin import customAdminSite
urlpatterns = [
    path('', views.Index.as_view()),
    path(r'api/', include(router.urls)),
    path('accounts/login/', views.Login.as_view()),
    path('accounts/logout/', views.logouts),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # path('api/ckeditor/client/upload', csrf_exempt(views.CKEditorUploadCloud.as_view()))
    path("api/graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # path('__debug__/', include(debug_toolbar.urls)),
]

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, Permission
from django.template.response import TemplateResponse
from django.urls import path
from oauth2_provider.models import AccessToken
from rest_framework.authtoken.models import Token

from .models import *


# Register your models here.


class UserAdminCustom(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'gender')

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj) + (
            (('Personal Custom'), {'fields': ('phone_number', 'gender')}),
        )


class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename", "content_type")
    list_filter = ("content_type",)


class EmotionAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "emotion_type"]


class EmotionPOSTAdmin(EmotionAdmin):

    def get_list_display(self, request):
        return self.list_display + [
            'post',
        ]


class EmotionContentAdmin(EmotionAdmin):

    def get_list_display(self, request):
        return self.list_display + [
            'comment',
        ]


class CustomAdminSite(admin.AdminSite):
    site_header = "Charity Social Network"
    index_title = site_header

    def get_urls(self):
        return [
                   path('stats', self.stats_view),
               ] + super().get_urls()

    def stats_view(self, request):
        count = User.objects.all().count()
        stats = 34

        self.title = 'page'
        return TemplateResponse(request,
                                'admin/newpage.html', {
                                    'course_count': count,
                                    'course_stats': stats
                                })


class HashtagInlinePost(admin.StackedInline):
    model = NewsPost.hashtag.through


class PostAdmin(admin.ModelAdmin):
    inlines = [HashtagInlinePost, ]
    list_display = ['id','title','user_id','user','category','is_show','active']


# admin.site.register(User, UserAdmin)
customAdminSite = CustomAdminSite(name='Charity Social Network')
customAdminSite.register(User,)
customAdminSite.register(Group, GroupAdmin)
customAdminSite.register(Permission,PermissionAdmin)
customAdminSite.register(
    [
        EmotionType,
        NewsCategory,
        Comment,
        ReportPost,
        AuctionItem,
        Transaction,
        OptionReport,
        Hashtag,
        HistoryAuction,ReportUser
    ])
customAdminSite.register(EmotionPost, EmotionPOSTAdmin)
customAdminSite.register(EmotionComment, EmotionContentAdmin)
customAdminSite.register(NewsPost, PostAdmin)

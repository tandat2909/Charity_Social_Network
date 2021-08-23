from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, Permission
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.safestring import mark_safe
from oauth2_provider.models import Application
from rest_framework.authtoken.models import Token

from .models import *


class CustomAdminSite(admin.AdminSite):
    site_header = "Charity Social Network"
    index_title = site_header
    index_template = "admin/index.html"

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
                                    'course_stats': stats,
                                    'add_list': self.get_app_list(request)
                                })


class BaseModelsAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/list.css',)
        }

        js = [
            'https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js',
            # 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js',
            # 'https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js',
            # 'https://cdn.datatables.net/v/dt/dt-1.10.25/datatables.min.js',
            'admin/js/database.js', ]


# Register your models here.


class UserAdminCustom(BaseModelsAdmin, UserAdmin):
    list_display = ['id', 'username', 'full_name', 'gender', 'birthday', 'email', 'is_staff',
                    'is_active',
                    'is_superuser', ]

    ordering = []
    search_fields = []
    readonly_fields = ["image", 'last_login', 'date_joined']

    fieldsets = (
        (_('Personal info'),
         {'fields': (
             'first_name', 'last_name', 'email', 'phone_number', 'nick_name', 'gender', 'avatar', 'image', 'last_login',
             'date_joined')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),

    )

    def full_name(self, user):
        return user.get_full_name()

    def image(self, user):
        return mark_safe('<img  style="width:200px;height: 200px;" src="{src}"/>'.format(src=user.avatar.url))


class PermissionAdmin(BaseModelsAdmin):
    list_display = ('id', "name", "codename", "content_type")
    list_filter = ("content_type",)
    list_per_page = 20


class GroupAdminCustom(BaseModelsAdmin, GroupAdmin):
    list_per_page = 12
    list_display = ["id", 'name']


class EmotionAdmin(BaseModelsAdmin):
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


class HashtagInlinePost(admin.StackedInline):
    model = NewsPost.hashtag.through


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = NewsPost
        fields = '__all__'


class PostAdmin(BaseModelsAdmin):
    form = PostForm
    inlines = [HashtagInlinePost, ]
    list_per_page = 20
    list_max_show_all = 60
    list_filter = ['created_date', 'user', 'category', 'is_show', ]
    list_display = ['title', 'user', 'full_name', 'category', 'created_date', "report", 'emotion', 'is_show',
                    'active', ]

    fieldsets = (
        (_('Thông tin Bài Viết'),
         {'fields': (
             'title', 'user', 'category', 'image', 'images', 'is_show', 'created_date', 'update_date'
         )}),
        (_('Nội dung'), {
            'fields': (
                'content',
            ),
        }),

    )
    readonly_fields = ['images', 'created_date', 'update_date']

    def full_name(self, post):
        return post.user.get_full_name()

    def report(self, post):
        amount = post.reports.all().count()
        return amount

    def emotion(self, post):
        amount = post.emotions.all().count()
        return amount

    def images(self, post):
        return mark_safe('<img  style="width:200px;height: 200px;" src="{src}"/>'.format(src=post.image.url))


class AuctionItemAdmin(BaseModelsAdmin):
    list_display = ['id', 'author', 'price_start', 'price_received', 'start_datetime', 'end_datetime', 'win', 'active',
                    'post']
    list_filter = ["start_datetime", 'end_datetime', 'post__category__name']

    def author(self, obj):
        return obj.post.user.get_full_name()

    def win(self, obj):
        try:
            return obj.receiver.get_full_name()
        except:
            return "Chưa chọn người chiến thắng"


class CommentAdmin(BaseModelsAdmin):
    list_display = ['id', "content", 'user', 'amount_emotion', 'amount_comment_child', 'active']

    def amount_emotion(self, obj):
        return obj.emotions.all().count()

    def amount_comment_child(self, obj):
        return obj.comment_child.all().count()




# admin.site.register(User, UserAdmin)
customAdminSite = CustomAdminSite(name='Charity Social Network')
customAdminSite.register(User, UserAdminCustom)
customAdminSite.register(Group, GroupAdminCustom)
customAdminSite.register(Permission, PermissionAdmin)
customAdminSite.register(
    [
        EmotionType,
        NewsCategory,

        ReportPost,
        Transaction,
        OptionReport,
        Hashtag,
        HistoryAuction, ReportUser
    ])
customAdminSite.register(EmotionPost, EmotionPOSTAdmin)
customAdminSite.register(EmotionComment, EmotionContentAdmin)
customAdminSite.register(NewsPost, PostAdmin)
customAdminSite.register(AuctionItem, AuctionItemAdmin)

customAdminSite.register(Comment, CommentAdmin)

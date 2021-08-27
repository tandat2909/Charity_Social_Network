from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import redirect_to_login
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
    context = {
        'count_notification': None,
        'title': "Dash Board"
    }

    def get_urls(self):
        return [
                   path('statistical', self.statistical_view),
                   path('dashboard', self.dashboard)
               ] + super().get_urls()

    def dashboard(self, request):
        if self.has_permission(request):
            context = self.get_context(request, "nav_dashboard")
            return TemplateResponse(request,
                                    'admin/Dashboard.html', context)
        return redirect_to_login(next='/admin/dashboard', login_url='/admin/login/')

    def statistical_view(self, request):
        if self.has_permission(request):
            context = self.get_context(request, nav_active="nav_statistical", title="Statistical")
            return TemplateResponse(request, 'admin/statistical.html', context)
        return redirect_to_login(next='/admin/statistical', login_url='/admin/login/')

    def get_context(self, request, nav_active, *args, **kwargs):
        self.context[nav_active] = "active"
        count_notification = request.user.notifications.filter(new=True).count()
        self.context["count_notification"] = count_notification
        self.context["title"] = kwargs.get("title", 'Dash Board')
        return self.context

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


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


class EmotionTypeAdmin(BaseModelsAdmin):
    list_display = ["id", 'name', 'description', 'created_date', 'active']


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


class AuctionItemInlinePost(admin.TabularInline):
    model = AuctionItem
    fk_name = "post"


class HistoryInlinePost(admin.TabularInline):
    model = HistoryAuction
    fk_name = "post"


class HashtagInlinePost(admin.StackedInline):
    model = NewsPost.hashtag.through


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = NewsPost
        fields = '__all__'


class PostAdmin(BaseModelsAdmin):
    form = PostForm
    inlines = [HashtagInlinePost, AuctionItemInlinePost, HistoryInlinePost]
    list_per_page = 20
    list_max_show_all = 60
    list_filter = ['created_date', 'user', 'category', 'is_show', ]
    list_display = ['id', 'title', 'user', 'full_name', 'category', 'created_date', "report", 'emotion', 'is_show',
                    'active', ]
    search_fields = ["user__username", 'user__first_name', 'user__last_name', "category__name", 'title']
    fieldsets = (
        (_('Thông tin Bài Viết'),
         {'fields': (
             'title', 'user', 'category', 'description', 'image', 'images', 'is_show', 'created_date', 'update_date'
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
    list_display = ['id', 'user', "content", 'amount_emotion', 'amount_comment_child', 'active']
    search_fields = ["content", "user__username", 'user__first_name', 'user__last_name']

    def amount_emotion(self, obj):
        return obj.emotions.all().count()

    def amount_comment_child(self, obj):
        return obj.comment_child.all().count()


class HashtagAdmin(BaseModelsAdmin):
    list_display = ["id", 'name', 'description', 'created_date', 'active']
    search_fields = ['name', 'description']
    list_filter = ["created_date", ]


class HistoryAuctionAdmin(BaseModelsAdmin):
    list_display = ['id', "post", 'user', 'price', 'created_date', 'update_date']
    search_fields = ["post__title", "user__username", "user__first_name", 'user__last_name']
    list_filter = ['user', 'post', 'price']


class CategoryPostAdmin(BaseModelsAdmin):
    list_display = ("id", "name", 'amount_post', 'description', 'created_date', 'active')

    def amount_post(self, cate):
        return cate.post.all().count()


class OptionReportAdmin(BaseModelsAdmin):
    list_display = ['id', "content"]


class ReportPostAdmin(BaseModelsAdmin):
    list_display = ["id", "user", 'reason', "content", 'post', 'created_date']
    list_filter = ["reason", 'user']
    search_fields = ["content", 'reason', 'user', 'post']


class ReportUserAdmin(BaseModelsAdmin):
    list_display = ["id", "user", 'reason', "content", 'user_report', 'created_date']
    list_filter = ["reason", 'user', 'user_report']
    search_fields = ["content", 'reason', 'user', 'user_report']


customAdminSite = CustomAdminSite(name='Charity Social Network')
customAdminSite.register(User, UserAdminCustom)
customAdminSite.register(Group, GroupAdminCustom)
customAdminSite.register(Permission, PermissionAdmin)
customAdminSite.register(
    [
        Transaction,
    ])
customAdminSite.register(EmotionPost, EmotionPOSTAdmin)
customAdminSite.register(EmotionType, EmotionTypeAdmin)
customAdminSite.register(EmotionComment, EmotionContentAdmin)
customAdminSite.register(NewsPost, PostAdmin)
customAdminSite.register(AuctionItem, AuctionItemAdmin)
customAdminSite.register(Comment, CommentAdmin)
customAdminSite.register(Hashtag, HashtagAdmin)
customAdminSite.register(HistoryAuction, HistoryAuctionAdmin)
customAdminSite.register(NewsCategory, CategoryPostAdmin)
customAdminSite.register(OptionReport, OptionReportAdmin)
customAdminSite.register(ReportPost, ReportPostAdmin)
customAdminSite.register(ReportUser, ReportUserAdmin)

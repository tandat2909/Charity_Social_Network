from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, Permission
from django.template.response import TemplateResponse
from django.urls import path

from .models import *


# Register your models here.





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


# admin.site.register(User, UserAdmin)
customAdminSite = CustomAdminSite(name='Charity Social Network')
customAdminSite.register(User, UserAdmin)
customAdminSite.register(Group, GroupAdmin)
customAdminSite.register(Permission)
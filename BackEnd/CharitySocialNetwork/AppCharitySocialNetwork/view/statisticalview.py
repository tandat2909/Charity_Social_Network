import datetime
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.http import HttpResponse

from ..models import NewsPost


class StatisticalViewSet(GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = NewsPost.objects.all()
    pagination_class = None

    def get_queryset(self):
        # trường hợp không phải admin
        if not self.request.user.is_superuser:
            return self.queryset.filter(user=self.request.user)
        # trường hợp admin
        return self.queryset

    @action(methods=["GET"], detail=False, url_path="post/(?P<year>[0-9]+)")
    def statistical_post(self, request, year, **kwargs):
        """
            Thông kê bài viết theo tháng theo từng năm
        """
        return Response(self.get_statistical_month_have_post_by_year(int(year)), status=status.HTTP_200_OK)

    def get_year_has_post(self):
        return [i.year for i in self.get_queryset().dates("created_date", "year", "DESC")]

    def get_statistical_month_have_post_by_year(self, year=datetime.datetime.now().year):
        """
            Count bài viết những tháng có bài viết theo năm truyền vào
            Mặc định sẽ lấy năm hiện tại
        :param year: chỉ định năm cần thống kê
        :return: return count has post nếu không có trả về mảng rỗng
        """
        if type(year) is int:
            data = {"months": {}}
            post_month = [i.month for i in
                          self.get_queryset().filter(created_date__year=year).dates("created_date", "month")]
            for m in post_month:
                data["months"][str(m)] = self.get_queryset().filter(created_date__year=year,
                                                                    created_date__month=m).count()
            return data
        return {"data": []}

    def get_statistical_day_have_post_by_month_year(self, year=datetime.datetime.now().year,
                                                    month=datetime.datetime.now().month):
        """
            Count bài viết những tháng có bài viết theo năm truyền vào
        :param month: chỉ định tháng cần thông kê
        :param year: chỉ định năm cần thống kê
        :return: return count has post nếu không có trả về mảng rỗng
        """
        if type(year) is int and type(month) is int:
            data = {"days": {}}
            queryset = self.get_queryset().filter(created_date__year=year, created_date__month=month)
            post_day = [i.day for i in queryset.dates("created_date", "day")]
            for d in post_day:
                data["days"][str(d)] = queryset.filter(created_date__day=d).count()
            return data
        return {"data": []}

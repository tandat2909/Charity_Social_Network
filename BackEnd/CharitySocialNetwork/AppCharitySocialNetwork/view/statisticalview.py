import datetime

from django.db.models import Q, Sum, Count, QuerySet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.http import HttpResponse

from ..models import NewsPost, Comment, NewsCategory


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
        cate = NewsCategory.objects.filter(active=True)

        data = []
        for c in cate:
            queryset = self.get_queryset().filter(category_id=c.id)
            data.append({
                "category": {
                    "id": c.id,
                    "name": c.name
                },
                "total": c.posts.count(),
                "data": self.get_statistical_month_have_post_by_year(queryset=queryset)
            })

        return Response(data, status=status.HTTP_200_OK)

    def get_year_has_post(self):
        return [i.year for i in self.get_queryset().dates("created_date", "year", "DESC")]

    def get_statistical_month_have_post_by_year(self, queryset=None, year=datetime.datetime.now().year):
        """
            Count bài viết những tháng có bài viết theo năm truyền vào
            Mặc định sẽ lấy năm hiện tại
        :param year: chỉ định năm cần thống kê
        :return: return count has post nếu không có trả về mảng rỗng
        """

        if type(year) is int:
            queryset = queryset or self.get_queryset()
            emotions = []
            comment = []
            month = []
            post = []
            post_month = [i.month for i in queryset.filter(created_date__year=year).dates("created_date", "month")]
            for m in post_month:
                posts = queryset.filter(created_date__year=year, created_date__month=m)
                # có tất cả bìa viết
                # lấy tất cả emotion theo bài viết
                count_emotion = posts.annotate(count_emotion=Count("emotionpost")).values("count_emotion")
                count_comment = posts.annotate(count_comment=Count("comment")).values("count_comment")

                emotions.append(sum(i.get("count_emotion") for i in count_emotion))
                comment.append(sum(i.get("count_comment") for i in count_comment))
                month.append(m)
                post.append(posts.count())

            data = {
                "month": month,
                "posts": post,
                "emotions": emotions,
                "comment": comment
            }
            return data

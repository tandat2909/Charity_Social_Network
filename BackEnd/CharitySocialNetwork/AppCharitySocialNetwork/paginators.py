from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class PostPagePagination(PageNumberPagination):
    page_size = settings.POST_PAGE_SIZE or PageNumberPagination.page_size or 30


class CommentPagePagination(PageNumberPagination):
    page_size = settings.COMMENT_PAGE_SIZE or PageNumberPagination.page_size or 30

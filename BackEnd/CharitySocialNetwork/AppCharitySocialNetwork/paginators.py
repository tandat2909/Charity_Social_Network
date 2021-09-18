from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class PostPagePagination(PageNumberPagination):
    page_size = settings.POST_PAGE_SIZE or PageNumberPagination.page_size or 30
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM
    max_page_size = settings.MAX_POST_PAGE_SIZE or 50


class CommentPagePagination(PageNumberPagination):
    page_size = settings.COMMENT_PAGE_SIZE or PageNumberPagination.page_size or 30
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM
    max_page_size = settings.MAX_COMMENT_PAGE_SIZE or 50


class NotificationPagePagination(PageNumberPagination):
    page_size = settings.NOTIFICATION_PAGE_SIZE or PageNumberPagination.page_size or 30
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM
    max_page_size = settings.MAX_NOTIFICATION_PAGE_SIZE or 50


class ImagePagePagination(PageNumberPagination):
    page_size = settings.IMAGE_PAGE_SIZE or PageNumberPagination.page_size or 30
    page_size_query_param = settings.PAGE_SIZE_QUERY_PARAM
    max_page_size = settings.MAX_IMAGE_PAGE_SIZE or 50

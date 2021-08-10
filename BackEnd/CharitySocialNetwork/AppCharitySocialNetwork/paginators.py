from rest_framework.pagination import PageNumberPagination
from . import settings


class PostPagePagination(PageNumberPagination):
    page_size = settings.POST_PAGE_SIZE or PageNumberPagination.page_size or None

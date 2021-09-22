from django.db.models import QuerySet


class BaseQuery:
    queryset = None

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

# class QuerySetModelBase:
#
#     def queryset_account(self, is_active=True, is_superuser=False, **kwargs):
#
#         """
#             Mặc định trả ra câu truy vấn queryset model User với tài khoản đang hoạt động is_active = True và không có quyền super
#             Nếu bạn muốn truy vấn thêm các user admin hoặc các user đã bị xóa thì thay đổi giá trị của các biến is_active và is_superuser
#             Tham số user_admin = True truy vấn thêm các user là superuser
#
#             :param is_superuser: bool
#             :param is_active: bool
#             :return Queryset<User>
#             :exception TypeError: when param [is_active or is_superuser] is not type bool
#         """
#
#         if type(is_active) is not bool:
#             raise TypeError("param is_active require type bool")
#
#         if type(is_superuser) is not bool:
#             raise TypeError("param is_superuser require type bool")
#
#         return User.objects.filter(is_active=is_active, is_superuser=is_superuser).all()
#
#     def queryset_post(self, active=True, **kwargs):
#         """
#             Mặc định trả ra câu truy vấn queryset model NewsPost chưa được xóa
#             Nếu muốn truy vấn các bài viết đã bị xóa cần thay đổi giá trị thuộc tính thành False
#
#         :param active: bool
#         :return: Queryset<NewsPost>
#         :exception TypeError: when param 'active' is not type bool
#         """
#         if type(active) is not bool:
#             raise TypeError("param is_active require type bool")
#         return NewsPost.objects.filter(active=active)
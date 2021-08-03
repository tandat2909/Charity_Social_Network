from rest_framework.permissions import IsAuthenticated


class PermissionUserViewInfo(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) \
               and request.user.has_perm('AppCharitySocialNetwork.view_user')


class PermissionUserChange(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) \
               and request.user.has_perm('AppCharitySocialNetwork.change_user')


class PermissionUserReport(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) \
               and request.user.has_perms([
            'AppCharitySocialNetwork.add_report',
            'AppCharitySocialNetwork.change_report',
            'AppCharitySocialNetwork.view_report',
            'AppCharitySocialNetwork.view_optionreport'
        ])


class PermissionUserMod(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) \
               and request.user.has_perms([
            'AppCharitySocialNetwork.mod',

        ])

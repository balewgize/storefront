from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """The request is authenticated as admin user, or is a read-only request."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    """Custom model permission to provide protection for GET request."""

    def __init__(self) -> None:
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]


class ViewCustomerHistoryPermission(permissions.BasePermission):
    """Custom model permission to view the history of a customer."""

    def has_permission(self, request, view):
        return request.user.has_perm("store.view_history")

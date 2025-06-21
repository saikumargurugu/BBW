from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedActiveUser(BasePermission):
    """
    Allows access only to authenticated users who are active.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsStaffUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_admin)



class IsInactiveAuthenticatedUser(BasePermission):
    """
    Allows access only to authenticated users who are inactive.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_active
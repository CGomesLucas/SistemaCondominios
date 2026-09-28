from rest_framework.permissions import BasePermission
from .models import Role


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.method in ("GET", "HEAD", "OPTIONS")
            or request.user.is_superuser
            or request.user.role == Role.ADMIN
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == Role.ADMIN or request.user.is_superuser)
        )


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == Role.CLIENT
        )


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )
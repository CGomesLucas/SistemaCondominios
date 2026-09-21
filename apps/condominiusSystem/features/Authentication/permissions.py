from rest_framework.permissions import BasePermission
from .models import User, Role


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.role(Role.ADMIN)
        )


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.role(Role.CLIENT)
        )


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(AdminOnly):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class ModerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_moder)
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin or request.user.is_moder:
            return True
        return obj.author == request.user


class IsModerOrReadOnly(ModerOnly):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or super().has_object_permission(request, view, obj)
        )

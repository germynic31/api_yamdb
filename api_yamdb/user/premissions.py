from rest_framework import permissions


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ModerPermisiion(permissions.BasePermission):

    def has_permission(self, request, view):
        role = request.user.role
        if (role == 'moder') or (role == 'admin') or (role == 'superuser'):
            return True


class AdminPermisiion(permissions.BasePermission):

    def has_permission(self, request, view):
        role = request.user.role
        if (role == 'admin') or (role == 'superuser'):
            return True


class SuperuserPermisiion(permissions.BasePermission):

    def has_permission(self, request, view):
        role = request.user.role
        if role == 'superuser':
            return True

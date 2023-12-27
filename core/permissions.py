from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and not request.user.is_staff and not request.user.is_superuser

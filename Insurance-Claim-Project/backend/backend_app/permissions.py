from rest_framework.permissions import BasePermission


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                    request.user.permission_level == 0) and not request.user.needs_approval


class IsFinance(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.permission_level == 1 or request.user.permission_level == 0) and not request.user.needs_approval


class IsAiEngineer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.permission_level == 2 or request.user.permission_level == 0) and not request.user.needs_approval


class IsEndUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.permission_level == 3 or request.user.permission_level == 0) and not request.user.needs_approval

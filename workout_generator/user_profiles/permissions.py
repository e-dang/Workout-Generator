from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff

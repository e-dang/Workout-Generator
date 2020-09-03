from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk', None)

        if pk is None:
            return False

        return pk == request.user.profile.pk

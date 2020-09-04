from rest_framework.permissions import IsAuthenticated


class IsOwner(IsAuthenticated):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk', None)

        if pk is None:
            return False

        return super().has_permission(request, view) and pk == request.user.profile.pk

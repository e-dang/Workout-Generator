from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from main.permissions import IsOwner, IsAdmin
from rest_framework.permissions import IsAdminUser


class ListRetrieveUpdateViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOwner | IsAdmin]

        return [permission() for permission in permission_classes]

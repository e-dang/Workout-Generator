from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Equipment
from .serializers import EquipmentSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsOwner
from main import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from .filters import EquipmentFilter


class UserEquipmentListView(ListCreateAPIView):
    serializer_class = EquipmentSerializer
    permission_classes = [IsOwner | IsAdminUser]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = EquipmentFilter
    search_fields = ['name', 'snames']
    ordering_fields = ['owner', 'name']
    ordering = ['name']

    def get_queryset(self):
        return Equipment.objects.available_to(self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        request.data['owner'] = kwargs.get('pk', None)
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipmentListView(ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_class = EquipmentFilter
    search_fields = ['name', 'snames']
    ordering_fields = ['owner', 'name']
    ordering = ['name']


class EquipmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsOwner | permissions.IsAdmin]

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Equipment
from .serializers import EquipmentSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsOwner
from main import permissions


class UserEquipmentListView(GenericAPIView):
    serializer_class = EquipmentSerializer
    permission_classes = [IsOwner | IsAdminUser]

    def get_queryset(self):
        return Equipment.objects.available_to(self.kwargs['pk'])  # important to use pk in case admin is issuing request

    def get(self, request, pk):
        serializer = self.get_serializer_class()(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        request.data['owner'] = pk  # important to use pk in case admin is issuing request
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EquipmentListView(ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminUser]


class EquipmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsOwner | permissions.IsAdmin]

from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Equipment, SharedEquipment
from .serializers import EquipmentSerializer
from django.http import Http404


class EquipmentListCreate(ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def list(self, request):
        """
        Get all pieces of equipment that have been shared with the User issuing the request.
        """

        equipment = [shared.equipment for shared in SharedEquipment.objects.filter(
            reciever=request.user.id).select_related('equipment')]
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class EquipmentDetail(APIView):
    def get_object(self, request, pk):
        try:
            return SharedEquipment.objects.get(equipment=pk, reciever=request.user.id).equipment
        except SharedEquipment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Get the piece of Equipment specified by the primary key and that has been shared with the User issuing the
        request.
        """

        equipment = self.get_object(request, pk)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        """
        Get the piece of Equipment specified by the primary key and that has been shared with the User issuing the
        request. Return a 404 response if that piece of Equipment does not exist or 401 response if that piece of
        Equipment does not belong to the User, else try to update the piece of Equipment's data. If the update is
        successful, return the new data and 200 response, else return the errors and a 400 response.
        """

        equipment = self.get_object(request, pk)

        if equipment.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = EquipmentSerializer(equipment, data=equipment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Get the piece of Equipment specified by the primary key and that has been shared with the User issuing the
        request. Return a 404 response if that piece of Equipment does not exist or 401 response if that piece of
        Equipment does not belong to the User, else delete the piece of Equipment and return a 204 response.
        """

        equipment = self.get_object(request, pk)

        if equipment.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        equipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

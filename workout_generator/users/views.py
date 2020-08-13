from rest_framework import generics, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        request.user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

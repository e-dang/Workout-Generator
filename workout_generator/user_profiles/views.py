from rest_framework.generics import RetrieveUpdateAPIView
from user_profiles.models import UserProfile
from user_profiles.serializers import UserProfileSerializer
from user_profiles.permissions import IsOwner, IsAdmin


class UserProfileDetail(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner | IsAdmin]

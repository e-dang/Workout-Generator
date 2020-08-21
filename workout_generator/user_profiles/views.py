from rest_framework.generics import RetrieveUpdateAPIView
from user_profiles.models import UserProfile
from user_profiles.serializers import UserProfileSerializer


class UserProfileDetail(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

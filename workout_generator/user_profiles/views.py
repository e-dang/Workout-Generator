from rest_framework.generics import RetrieveAPIView
from user_profiles.models import UserProfile
from user_profiles.serializers import UserProfileSerializer


class UserProfileDetail(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

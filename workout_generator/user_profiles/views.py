from user_profiles.models import UserProfile
from user_profiles.serializers import UserProfileSerializer
from main.viewsets import ListRetrieveUpdateViewSet


class UserProfileViewSet(ListRetrieveUpdateViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

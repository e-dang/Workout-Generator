from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from user_profiles.models import UserProfile
from user_profiles.serializers import UserProfileSerializer
from django_filters import rest_framework as filters
from main.permissions import IsAdmin, IsOwner
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import OrderingFilter
from user_profiles.filters import UserProfileFilter


class UserProfileListView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = UserProfileFilter
    ordering_fields = ('id', 'gender', 'weight', 'height', 'bmi', 'visibility',
                       'user__id', 'user__first_name', 'user__last_name')
    ordering = ('id',)


class UserProfileDetailView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner | IsAdmin]

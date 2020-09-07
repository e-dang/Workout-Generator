from django_filters import rest_framework as filters
from user_profiles.models import UserProfile


class UserProfileFilter(filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            'gender': ['iexact'],
            'weight': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'height': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'bmi': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'visibility': ['iexact'],
            'user__first_name': ['iexact', 'contains'],
            'user__last_name': ['iexact', 'contains']
        }

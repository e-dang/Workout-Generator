from django.urls import path
from user_profiles.views import UserProfileListView, UserProfileDetailView

urlpatterns = [
    path('', UserProfileListView.as_view(), name='profile-list'),
    path('<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail')
]

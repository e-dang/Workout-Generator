from django.urls import path
from user_profiles.views import UserProfileDetail

urlpatterns = [
    path('<int:pk>/', UserProfileDetail.as_view(), name='profile-detail')
]

from django.urls import path, include
from user_profiles.views import UserProfileListView, UserProfileDetailView
from equipment.views import UserEquipmentListView

urlpatterns = [
    path('', UserProfileListView.as_view(), name='profile-list'),
    path('<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('<int:pk>/equipment/', UserEquipmentListView.as_view(), name='user-equipment-list')
]

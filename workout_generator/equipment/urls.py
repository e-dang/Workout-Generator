from django.urls import path
from .views import EquipmentListView, EquipmentDetailView

urlpatterns = [
    path('', EquipmentListView.as_view(), name='equipment-list'),
    path('<int:pk>/', EquipmentDetailView.as_view(), name='equipment-detail')
]

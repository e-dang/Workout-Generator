from django.urls import path
from .views import EquipmentListCreate, EquipmentDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', EquipmentListCreate.as_view(), name='equipment-list'),
    path('<int:pk>/', EquipmentDetail.as_view(), name='equipment-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)

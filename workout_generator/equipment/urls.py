from django.urls import path
from .views import EquipmentListView, EquipmentDetailView

urlpatterns = [
    path('', EquipmentListView.as_view()),
    path('<int:pk>/', EquipmentDetailView.as_view())
]

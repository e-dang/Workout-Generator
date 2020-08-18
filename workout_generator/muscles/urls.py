from django.urls import path
import muscles.views as views

urlpatterns = [
    path('subportion/', views.MuscleSubPortionList.as_view(), name='muscle-subportion-list'),
    path('subportion/<str:pk>/', views.MuscleSubPortionDetail.as_view(), name='muscle-subportion-detail'),
    path('muscle/', views.MuscleList.as_view(), name='muscle-list'),
    path('muscle/<str:pk>/', views.MuscleDetail.as_view(), name='muscle-detail'),
    path('grouping/', views.MuscleGroupingList.as_view(), name='muscle-grouping-list'),
    path('grouping/<str:pk>/', views.MuscleGroupingDetail.as_view(), name='muscle-grouping-detail')
]

from django.urls import path
import muscles.views as views

urlpatterns = [
    path('subportion/', views.MuscleSubPortionList.as_view()),
    path('subportion/<str:pk>/', views.MuscleSubPortionDetail.as_view()),
    path('muscle/', views.MuscleList.as_view()),
    path('muscle/<str:pk>/', views.MuscleDetail.as_view()),
    path('muscle-grouping/', views.MuscleGroupingList.as_view()),
    path('muscle-grouping/<str:pk>/', views.MuscleGroupingDetail.as_view())
]

from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include, path

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    include('', include(router.urls))
]

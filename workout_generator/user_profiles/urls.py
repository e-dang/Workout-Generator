from user_profiles.views import UserProfileViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', UserProfileViewSet, basename='profile')

urlpatterns = router.urls

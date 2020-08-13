from .views import UserDeleteView
from django.urls import include, path
from rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('delete/', UserDeleteView.as_view()),
    path('registration/', include('rest_auth.registration.urls')),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]

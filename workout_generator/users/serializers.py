from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
import rest_auth.registration.serializers as reg_serializers
import rest_auth.serializers as auth_serializers
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'email', 'first_name', 'last_name')


class RegisterSerializer(reg_serializers.RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True, write_only=True, max_length=20)
    last_name = serializers.CharField(required=True, write_only=True, max_length=20)

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('First name can only contain letters')

        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Last name can only contain letters')

        return value

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['first_name'] = self.validated_data.get('first_name', '')
        cleaned_data['last_name'] = self.validated_data.get('last_name', '')
        return cleaned_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class LoginSerializer(auth_serializers.LoginSerializer):
    username = None

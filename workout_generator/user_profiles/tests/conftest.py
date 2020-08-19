import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return 'strong-test-pass123'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    """
    Taken from https://djangostars.com/blog/django-pytest-testing/
    """

    def make_user(**kwargs):
        kwargs['email'] = kwargs.get('email', 'JohnDoe@demo.com')
        kwargs['password'] = test_password
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def auto_login_user(db, api_client, create_user):
    """
    Taken from https://djangostars.com/blog/django-pytest-testing/
    """

    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return api_client, user

    return make_auto_login

import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.management import call_command
from workout_generator.urls import PREFIX_API_URL


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

    def make_auto_login(user=None, **kwargs):
        if user is None:
            user = create_user(**kwargs)
        token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return api_client, user

    return make_auto_login


@pytest.fixture
def auto_login_profile(auto_login_user):
    def convert_user_to_profile(**kwargs):
        kwargs['weight'] = kwargs.get('weight', 160)
        kwargs['height'] = kwargs.get('height', 60)
        kwargs['bmi'] = kwargs.get('bmi', 12)
        api_client, user = auto_login_user(**kwargs)
        return api_client, user.profile
    return convert_user_to_profile


@pytest.fixture
def global_user(db):
    call_command('create_global_user')


@pytest.fixture
def init_muscles(db):
    call_command('init_muscles')


def add_api_prefix(suburl):
    return f'/{PREFIX_API_URL}{suburl}'

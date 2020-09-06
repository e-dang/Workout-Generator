import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.management import call_command
from . import factories
from pytest_factoryboy import register


@pytest.fixture(scope='session')
def faker_seed():
    return 12345


register(factories.AutoCreateUserFactory)
register(factories.UserProfileFactory)
register(factories.UserFactory)
register(factories.FollowingFactory)
register(factories.FollowRequestFactory)
register(factories.EquipmentFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return factories.TEST_PASSWORD


@pytest.fixture
def auto_login_user(db, api_client, auto_create_user_factory):
    def make_auto_login(user=None, **kwargs):
        if user is None:
            user = auto_create_user_factory(**kwargs)
        token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return api_client, user

    return make_auto_login


@pytest.fixture
def auto_login_profile(user_profile_factory, auto_login_user):
    def convert_user_to_profile(**kwargs):
        profile = user_profile_factory(**kwargs)
        api_client, _ = auto_login_user(user=profile.user)
        return api_client, profile
    return convert_user_to_profile


@pytest.fixture
def global_user(db):
    call_command('create_global_user')


@pytest.fixture
def init_muscles(db):
    call_command('init_muscles')

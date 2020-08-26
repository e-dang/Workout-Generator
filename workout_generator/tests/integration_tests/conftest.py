import pytest
import mock

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.management import call_command
from user_profiles.models import UserProfile


class UserGenerator:
    def __init__(self, db, django_user_model, test_password, request):
        self.db = db
        self.django_user_model = django_user_model
        self.test_password = test_password
        self.method = getattr(request, 'param', False)
        self.count = 0

    def get_factory_method(self):
        if self.method:
            return self.create_user_no_auto_follow
        else:
            return self.create_user

    def get_next_email(self):
        self.count += 1
        return f'JohnDoe{self.count - 1}@demo.com'

    def create_user(self, **kwargs):
        kwargs['email'] = kwargs.get('email', self.get_next_email())
        kwargs['password'] = self.test_password
        return self.django_user_model.objects.create_user(**kwargs)

    def create_user_no_auto_follow(self, **kwargs):
        func = UserProfile.objects.create

        def side_effect(*args, **kwargs):
            func(*args, **kwargs)
            return mock.DEFAULT

        kwargs['email'] = kwargs.get('email', self.get_next_email())
        kwargs['password'] = self.test_password
        with mock.patch('user_profiles.signals.UserProfile.objects.create') as mock_create, \
                mock.patch('user_profiles.signals.UserProfile.objects.get'):
            mock_create.return_value = mock.MagicMock()
            mock_create.side_effect = side_effect
            return self.django_user_model.objects.create_user(**kwargs)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return 'strong-test-pass123'


@pytest.fixture
def create_user(db, django_user_model, test_password, request):
    return UserGenerator(db, django_user_model, test_password, request).get_factory_method()


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

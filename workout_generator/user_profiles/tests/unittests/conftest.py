import mock
import pytest

from user_profiles.models import UserProfile


@pytest.fixture
def create_user(db, django_user_model, test_password):
    func = UserProfile.objects.create

    def side_effect(*args, **kwargs):
        func(*args, **kwargs)
        return mock.DEFAULT

    def make_user(**kwargs):
        kwargs['email'] = kwargs.get('email', 'JohnDoe@demo.com')
        kwargs['password'] = test_password
        with mock.patch('user_profiles.signals.UserProfile.objects.create') as mock_create, \
                mock.patch('user_profiles.signals.UserProfile.objects.get'):
            mock_create.return_value = mock.MagicMock()
            mock_create.side_effect = side_effect
            return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_profile(auto_login_user):
    def convert_user_to_profile(**kwargs):
        kwargs['weight'] = kwargs.get('weight', 160)
        kwargs['height'] = kwargs.get('height', 60)
        kwargs['bmi'] = kwargs.get('bmi', 12)
        api_client, user = auto_login_user(**kwargs)
        return api_client, user.profile
    return convert_user_to_profile

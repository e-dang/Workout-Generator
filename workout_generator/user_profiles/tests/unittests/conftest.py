import mock
import pytest

from user_profiles.models import UserProfile


@pytest.fixture
def create_user_no_follow(db, django_user_model, test_password):
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

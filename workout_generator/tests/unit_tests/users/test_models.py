import pytest
import mock

from django.core.exceptions import FieldDoesNotExist
from users.models import User
from users.managers import UserManager


def test_user_doesnt_have_user_name():
    user = User(email='test@demo.com', password='testpass')

    with pytest.raises(FieldDoesNotExist):
        _ = user._meta.get_field('username')


def test_user_email_verbose_name():
    user = User(email='test@demo.com', password='testpass')

    assert user._meta.get_field('email').verbose_name == 'email'


def test_user_uses_email_as_username():
    assert User.USERNAME_FIELD == 'email'


def test_user_required_fields():
    assert User.REQUIRED_FIELDS == []


def test_user_str():
    mock_user = mock.MagicMock(spec=User)
    mock_user.email = 'test@demo.com'

    assert User.__str__(mock_user) == 'test@demo.com'


def test_user_has_expected_manager():
    assert isinstance(User.objects, UserManager)

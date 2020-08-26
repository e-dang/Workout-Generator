import pytest

from users.managers import UserManager


@pytest.mark.parametrize('email', [
    '',
    None,
    False,
    []
],
    ids=['empty string', 'None', 'boolean', 'empty list'])
def test_user_manager_create_user_fail(email):
    manager = UserManager()

    with pytest.raises(ValueError):
        _ = manager.create_user(email, 'password123')


@pytest.mark.parametrize('extra_fields, err_msg', [
    ({'is_staff': False}, 'is_staff=True'),
    ({'is_superuser': False}, 'is_superuser=True')
],
    ids=['not staff', 'not superuser'])
def test_user_manager_create_superuser_fail(extra_fields, err_msg):
    manager = UserManager()

    with pytest.raises(ValueError) as err:
        _ = manager.create_superuser('JohnDoe@demo.com', 'thisisatest123', **extra_fields)

    assert err_msg in str(err.value)

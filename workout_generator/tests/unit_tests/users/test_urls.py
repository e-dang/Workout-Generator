from rest_framework.reverse import reverse
from tests.conftest import add_api_prefix


def test_user_detail_url():
    assert reverse('rest_user_details') == add_api_prefix('users/user/')


def test_login_url():
    assert reverse('rest_login') == add_api_prefix('users/login/')


def test_logout_url():
    assert reverse('rest_logout') == add_api_prefix('users/logout/')


def test_user_registration_url():
    assert reverse('rest_register') == add_api_prefix('users/registration/')


def test_delete_url():
    assert reverse('delete-user') == add_api_prefix('users/delete/')


def test_password_reset_url():
    assert reverse('rest_password_reset') == add_api_prefix('users/password/reset/')


def test_password_reset_confirm_url():
    assert reverse('rest_password_reset_confirm') == add_api_prefix('users/password/reset/confirm/')


def test_password_change_url():
    assert reverse('rest_password_change') == add_api_prefix('users/password/change/')


def test_password_reset_confirm_with_tokens():
    uuid = 'uuid'
    token = 'reset-token'
    assert reverse('password_reset_confirm', kwargs={'uidb64': uuid,
                                                     'token': token}) == add_api_prefix(f'users/password-reset-confirm/{uuid}/{token}/')

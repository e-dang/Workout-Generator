import pytest
import mock
from user_profiles.permissions import IsOwner, IsAdmin


def test_is_owner_has_object_permission():
    mock_request = mock.MagicMock()
    mock_obj = mock.MagicMock()
    mock_view = mock.MagicMock()
    mock_user = mock.MagicMock()
    permissions = IsOwner()

    mock_request.user = mock_user
    mock_obj.user = mock_user

    assert permissions.has_object_permission(mock_request, mock_view, mock_obj)


def test_is_owner_doesnt_have_object_permission():
    mock_request = mock.MagicMock()
    mock_obj = mock.MagicMock()
    mock_view = mock.MagicMock()
    mock_user1 = mock.MagicMock()
    mock_user2 = mock.MagicMock()
    permissions = IsOwner()

    mock_request.user = mock_user1
    mock_obj.user = mock_user2

    assert not permissions.has_object_permission(mock_request, mock_view, mock_obj)


@pytest.mark.parametrize('is_admin', [
    True,
    False
],
    ids=['is admin', 'is not admin'])
def test_is_admin_has_object_permission(is_admin):
    mock_request = mock.MagicMock()
    mock_view = mock.MagicMock()
    mock_object = mock.MagicMock()
    permissions = IsAdmin()

    mock_request.user.is_staff = is_admin

    assert permissions.has_object_permission(mock_request, mock_view, mock_object) is is_admin


@pytest.mark.parametrize('permission', [
    IsOwner,
    IsAdmin
],
    ids=['IsOwner', 'IsAdmin'])
@pytest.mark.parametrize('is_authenticated', [
    True,
    False
],
    ids=['is authenticated', 'is not authenticated'])
def test_has_permission(permission, is_authenticated):
    mock_request = mock.MagicMock()
    mock_view = mock.MagicMock()
    permissions = permission()

    mock_request.user.is_authenticated = is_authenticated

    assert permissions.has_permission(mock_request, mock_view) is is_authenticated

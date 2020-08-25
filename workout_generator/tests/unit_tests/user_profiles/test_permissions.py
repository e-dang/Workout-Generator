import mock
from user_profiles.permissions import IsOwner


def test_is_owner_has_permission():
    mock_request = mock.MagicMock()
    mock_obj = mock.MagicMock()
    mock_view = mock.MagicMock()
    mock_user = mock.MagicMock()
    permissions = IsOwner()

    mock_request.user = mock_user
    mock_obj.user = mock_user

    assert permissions.has_object_permission(mock_request, mock_view, mock_obj)


def test_is_owner_doesnt_have_permission():
    mock_request = mock.MagicMock()
    mock_obj = mock.MagicMock()
    mock_view = mock.MagicMock()
    mock_user1 = mock.MagicMock()
    mock_user2 = mock.MagicMock()
    permissions = IsOwner()

    mock_request.user = mock_user1
    mock_obj.user = mock_user2

    assert not permissions.has_object_permission(mock_request, mock_view, mock_obj)

import pytest
import mock

from users.adapters import AccountAdapter


@pytest.mark.parametrize('commit', [
    True,
    False
],
    ids=['commited', 'not commited'])
def test_account_adapter_save_user(commit):
    mock_adapter = mock.MagicMock(spec=AccountAdapter)
    mock_super = mock.MagicMock()
    mock_user1 = mock.MagicMock()
    mock_user2 = mock.MagicMock()
    mock_form = mock.MagicMock()
    mock_request = mock.MagicMock()
    mock_super.save_user.return_value = mock_user2
    mock_form.cleaned_data = {
        'email': 'JohnDoe@demo.com', 'password': 'password123', 'first_name': 'John', 'last_name': 'Doe'}

    with mock.patch('users.adapters.super', return_value=mock_super):
        user = AccountAdapter.save_user(mock_adapter, mock_request, mock_user1, mock_form, commit=commit)

        assert user is mock_user2
        mock_super.save_user.assert_called_once_with(mock_request, mock_user1, mock_form, commit)
        assert user.first_name == mock_form.cleaned_data['first_name']
        assert user.last_name == mock_form.cleaned_data['last_name']
        mock_user2.save.assert_called_once()

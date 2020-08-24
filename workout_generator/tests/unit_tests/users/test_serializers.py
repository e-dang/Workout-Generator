import mock
import pytest
import rest_auth.registration.serializers as reg_serializers
from rest_framework.serializers import ValidationError

from users.models import User
from users.serializers import RegisterSerializer, UserSerializer, LoginSerializer


def test_user_serializer_meta_model():
    serializer = UserSerializer()

    assert serializer.Meta.model is User


def test_user_serializer_meta_fields():
    serializer = UserSerializer()

    assert serializer.Meta.fields == ('id', 'email', 'first_name', 'last_name')


@pytest.mark.parametrize('method', [
    'validate_first_name',
    'validate_last_name'
], ids=['validate_first_name', 'validate_last_name'])
@pytest.mark.parametrize('name', [
    'test',
    'TEST',
    'Test'
],
    ids=['lower case', 'uppcase', 'hybrid case'])
def test_register_serializer_validate_name(method, name):
    serializer = RegisterSerializer()

    assert getattr(serializer, method)(name) == name


@pytest.mark.parametrize('method, err_msg', [
    ('validate_first_name', 'firstname'),
    ('validate_last_name', 'lastname')
], ids=['validate_first_name', 'validate_last_name'])
@pytest.mark.parametrize('name', [
    'test1',
    'te st',
    'te.st',
    '__test__',
    'test\t',
    'test\n'
],
    ids=['numeric char', 'space char', 'period char', 'underscore char', 'tab', 'new line'])
def test_register_serializer_validate_name_fail(method, err_msg, name):
    serializer = RegisterSerializer()

    with pytest.raises(ValidationError) as err:
        _ = getattr(serializer, method)(name)

    assert err_msg in str(err.value).lower().replace(' ', '')


@pytest.mark.parametrize('validated_data, expected', [
    ({'first_name': 'John', 'last_name': 'Doe'}, {'email': 'JohnDoe@demo.com',
                                                  'password': 'password123', 'first_name': 'John', 'last_name': 'Doe'}),
    ({'first_name': 'John'}, {'email': 'JohnDoe@demo.com',
                              'password': 'password123', 'first_name': 'John', 'last_name': ''}),
    ({'last_name': 'Doe'}, {'email': 'JohnDoe@demo.com',
                            'password': 'password123', 'first_name': '', 'last_name': 'Doe'})
],
    ids=['both names', 'first name', 'last name'])
def test_register_serializer_get_cleaned_data(validated_data, expected):
    mock_super = mock.MagicMock(spec=reg_serializers.RegisterSerializer)
    mock_super.get_cleaned_data.return_value = {'email': 'JohnDoe@demo.com', 'password': 'password123'}
    mock_serializer = mock.MagicMock(spec=RegisterSerializer)
    mock_serializer.validated_data = validated_data

    with mock.patch('users.serializers.super', return_value=mock_super):
        cleaned_data = RegisterSerializer.get_cleaned_data(mock_serializer)

        assert cleaned_data == expected
        mock_super.get_cleaned_data.assert_called_once()


def test_register_serializer_save():
    mock_serializer = mock.MagicMock(spec=RegisterSerializer)
    mock_request = mock.MagicMock()
    mock_adpater = mock.MagicMock()
    mock_user = mock.MagicMock()
    mock_serializer.get_cleaned_data.return_value = {
        'email': 'JohnDoe@demo.com', 'password': 'password123', 'first_name': 'John', 'last_name': 'Doe'}
    mock_adpater.new_user.return_value = mock_user
    with mock.patch('users.serializers.get_adapter', return_value=mock_adpater), \
            mock.patch('users.serializers.setup_user_email') as mock_setup_email:
        user = RegisterSerializer.save(mock_serializer, mock_request)

        mock_adpater.new_user.assert_called_once_with(mock_request)
        mock_serializer.get_cleaned_data.assert_called_once()
        mock_adpater.save_user.assert_called_once_with(mock_request, mock_user, mock_serializer)
        mock_setup_email.assert_called_once_with(mock_request, mock_user, [])
        mock_user.save.assert_called_once()
        assert user is mock_user


def test_login_serializer_doesnt_have_username():
    serializer = LoginSerializer()

    assert 'username' not in serializer.get_fields()

import pytest
import mock

from django.core.exceptions import ValidationError
from users.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms


@pytest.mark.parametrize('field_name, label', [
    ('password1', 'Password'),
    ('password2', 'Password Confirmation')
],
    ids=['password1', 'password2'])
def test_user_creation_form_password_label(field_name, label):
    form = UserCreationForm()

    assert form.fields[field_name].label == label


@pytest.mark.parametrize('field_name', [
    'password1',
    'password2'
],
    ids=['password1', 'password2'])
def test_user_creation_form_password_widget(field_name):
    form = UserCreationForm()

    assert isinstance(form.fields[field_name].widget, forms.PasswordInput)


def test_user_creation_form_model_is_expected():
    form = UserCreationForm()

    assert form.Meta.model is User


def test_user_creation_form_meta_fields():
    form = UserCreationForm()

    assert form.Meta.fields == ('email', 'first_name', 'last_name')


@pytest.mark.parametrize('data', [
    {'password1': 'password123', 'password2': 'password123'},
    {'password2': 'password123'},
    {'password1': 'password123'}
],
    ids=['matching passwords', 'missing password1', 'missing password2'])
def test_user_creation_form_clean_password2(data):
    mock_form = mock.MagicMock(spec=UserCreationForm)
    mock_form.cleaned_data = data

    assert UserCreationForm.clean_password2(mock_form) == data.get('password2')


def test_user_creation_form_clean_password2_fail():
    mock_form = mock.MagicMock(spec=UserCreationForm)
    mock_form.cleaned_data = {'password1': 'first_password', 'password2': 'second_password'}

    with pytest.raises(ValidationError):
        UserCreationForm.clean_password2(mock_form)


@pytest.mark.parametrize('commit', [
    True,
    False
],
    ids=['commit', 'no commit'])
def test_user_creation_form_save(commit):
    mock_super = mock.MagicMock()
    with mock.patch('users.forms.super', return_value=mock_super):
        mock_form = mock.MagicMock(spec=UserCreationForm)
        mock_form.cleaned_data = {'password1': 'password123'}
        mock_user = mock.MagicMock()
        mock_super.save.return_value = mock_user

        user = UserCreationForm.save(mock_form, commit)

        assert mock_user is user
        mock_super.save.assert_called_once()
        mock_super.save.assert_called_with(commit=False)
        mock_user.set_password.assert_called_once()
        mock_user.set_password.assert_called_with(mock_form.cleaned_data['password1'])
        if commit:
            mock_user.save.assert_called_once()
        else:
            mock_user.save.assert_not_called()

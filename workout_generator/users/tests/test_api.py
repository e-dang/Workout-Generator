import pytest

from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from users.models import User


def invalidate_credentials(api_client):
    api_client.credentials(HTTP_AUTHORIZATION='Token INVALID_TOKEN')


@pytest.mark.django_db
def test_login(api_client, create_user, test_password):
    url = reverse('rest_login')
    user = create_user()

    resp = api_client.post(url, {'email': user.email, 'password': test_password})

    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert 'key' in resp.data
    assert len(resp.data['key']) == 40


@pytest.mark.django_db
def test_login_fail(api_client, create_user):
    url = reverse('rest_login')
    user = create_user()

    resp = api_client.post(url, {'email': user.email, 'password': 'THE_WRONG_PASSWORD'})

    assert resp.status_code == 400


@pytest.mark.django_db
def test_logout(auto_login_user):
    url = reverse('rest_logout')
    api_client, _ = auto_login_user()

    resp = api_client.post(url)

    assert resp.status_code == 200
    assert len(Token.objects.all()) == 0


@pytest.mark.django_db
def test_logout_fail(auto_login_user):
    url = reverse('rest_logout')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)

    resp = api_client.post(url)

    assert resp.status_code == 401
    assert len(resp.data) == 1
    assert 'Invalid token.' in resp.data['detail']
    assert len(Token.objects.all()) == 1


@pytest.mark.parametrize('api_client, data', [
    (None, {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John', 'last_name': 'Doe'}),
    (None, {'email': 'Johnoe@demo.com', 'password1': 'thisisatest123', 'password2': 'thisisatest123'}),
],
    indirect=['api_client'],
    ids=['with names', 'without names'])
@pytest.mark.django_db
def test_registration(api_client, data):
    url = reverse('rest_register')

    resp = api_client.post(url, data)

    assert resp.status_code == 201
    user = User.objects.get(email=data['email'])
    assert user
    assert len(User.objects.all()) == 1
    assert resp.data['key'] == Token.objects.get(user=user.id).key


@pytest.mark.parametrize('api_client, data, error_field', [
    (None, {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John1', 'last_name': 'Doe'}, 'first_name'),
    (None, {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John!', 'last_name': 'Doe'}, 'first_name'),
    (None, {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'Johnaaaaaaaaaaaaaaaaa', 'last_name': 'Doe'}, 'first_name'),
    (None, {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John', 'last_name': 'Doe1'}, 'last_name'),
    (None, {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John', 'last_name': 'Doe!'}, 'last_name'),
    (None, {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John', 'last_name': 'Doeaaaaaaaaaaaaaaaaaa'}, 'last_name'),
    (None, {'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John', 'last_name': 'Doe!'}, 'email'),
    (None, {'email': 'JohnDoe@demo.com',
            'password2': 'thisisatest123', 'first_name': 'John', 'last_name': 'Doe!'}, 'password1'),
    (None, {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'first_name': 'John', 'last_name': 'Doe!'}, 'password2'),
],
    indirect=['api_client'],
    ids=['first name with number', 'first name with symbol', 'first name too long', 'last name with number',
         'last name with symbol', 'last name too long', 'missing_email', 'missing_password1', 'missing_password2'
         ])
@pytest.mark.django_db
def test_registration_fail_invalid_fields(api_client, data, error_field):
    url = reverse('rest_register')

    resp = api_client.post(url, data)

    assert resp.status_code == 400
    assert error_field in resp.data


@pytest.mark.django_db
def test_registration_fail_duplicate_email(api_client):
    url = reverse('rest_register')
    data = {'email': 'JohnDoe@demo.com', 'password1': 'thisisatest123',
            'password2': 'thisisatest123', 'first_name': 'John', 'last_name': 'Doe'}

    _ = api_client.post(url, data)
    resp = api_client.post(url, data)

    assert resp.status_code == 400
    assert 'email' in resp.data


@pytest.mark.django_db
def test_user_delete(auto_login_user):
    url = reverse('delete-user')
    api_client, _ = auto_login_user()

    resp = api_client.delete(url)

    assert resp.status_code == 204
    assert len(User.objects.all()) == 0


@pytest.mark.django_db
def test_user_delete_fail(auto_login_user):
    url = reverse('delete-user')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)

    resp = api_client.delete(url)

    assert resp.status_code == 401
    assert len(User.objects.all()) == 1
    assert 'Invalid token.' in resp.data['detail']


@pytest.mark.django_db
def test_user_detail_get(auto_login_user):
    url = reverse('rest_user_details')
    api_client, user = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert resp.data['email'] == user.email
    assert resp.data['first_name'] == user.first_name
    assert resp.data['last_name'] == user.last_name


@pytest.mark.django_db
def test_user_detail_get_fail_not_logged_in(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)

    resp = api_client.get(url)

    assert resp.status_code == 401
    assert 'Invalid token.' in resp.data['detail']


@pytest.mark.django_db
def test_user_detail_put(auto_login_user):
    url = reverse('rest_user_details')
    api_client, user = auto_login_user()
    data = {'email': user.email, 'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.put(url, data)

    assert resp.status_code == 200
    assert resp.data['email'] == data['email']
    assert resp.data['first_name'] != user.first_name
    assert resp.data['last_name'] != user.last_name
    assert resp.data['first_name'] == data['first_name']
    assert resp.data['last_name'] == data['last_name']


@pytest.mark.django_db
def test_user_detail_put_fail_not_logged_in(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)
    data = {'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.put(url, data)

    assert resp.status_code == 401
    assert 'Invalid token.' in resp.data['detail']


@pytest.mark.django_db
def test_user_detail_put_fail_not_full_state(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    data = {'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.put(url, data)

    assert resp.status_code == 400


@pytest.mark.django_db
def test_user_detail_patch(auto_login_user):
    url = reverse('rest_user_details')
    api_client, user = auto_login_user()
    data = {'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.patch(url, data)

    assert resp.status_code == 200
    assert resp.data['email'] == user.email
    assert resp.data['first_name'] != user.first_name
    assert resp.data['last_name'] != user.last_name
    assert resp.data['first_name'] == data['first_name']
    assert resp.data['last_name'] == data['last_name']


@pytest.mark.django_db
def test_user_detail_patch_fail_not_logged_in(auto_login_user):
    url = reverse('rest_user_details')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)
    data = {'first_name': 'new_first_name', 'last_name': 'new_last_name'}

    resp = api_client.patch(url, data)

    assert resp.status_code == 401
    assert 'Invalid token.' in resp.data['detail']


@pytest.mark.django_db
def test_user_change_password(auto_login_user, test_password):
    url = reverse('rest_password_change')
    api_client, user = auto_login_user()
    new_password = 'thisisanewpassword123'
    data = {'new_password1': new_password, 'new_password2': new_password, 'old_password': test_password}

    resp = api_client.post(url, data)

    assert resp.status_code == 200
    assert User.objects.get(email=user.email).check_password(new_password)


@pytest.mark.django_db
def test_user_change_password_fail_not_logged_in(auto_login_user, test_password):
    url = reverse('rest_password_change')
    api_client, _ = auto_login_user()
    invalidate_credentials(api_client)
    new_password = 'thisisanewpassword123'
    data = {'new_password1': new_password, 'new_password2': new_password, 'old_password': test_password}

    resp = api_client.post(url, data)

    assert resp.status_code == 401
    assert 'Invalid token.' in resp.data['detail']


@pytest.mark.parametrize('auto_login_user, test_password, data, error_field', [
    (None, None, {'new_password2': 'a_different_test_password123', 'old_password': None}, 'new_password1'),
    (None, None, {'new_password1': 'a_unique_test_password123', 'old_password': None}, 'new_password2'),
    (None, None, {'new_password1': 'a_unique_test_password123',
                  'new_password2': 'a_unique_test_password123'}, 'old_password'),
    (None, None, {'new_password1': 'a_unique_test_password123',
                  'new_password2': 'a_different_test_password123', 'old_password': None}, 'new_password2'),
    (None, None, {'new_password1': 'a_unique_test_password123',
                  'new_password2': 'a_unique_test_password123', 'old_password': 'invalid_password'}, 'old_password')
],
    indirect=['auto_login_user', 'test_password'],
    ids=['missing new_password1', 'missing new_password2', 'missing old_password', 'mismatching new passwords', 'invalid old_password'])
@pytest.mark.django_db
def test_user_change_password_fail_invalid_input(auto_login_user, test_password, data, error_field):
    url = reverse('rest_password_change')
    api_client, _ = auto_login_user()
    if 'old_password' in data and data['old_password'] is None:
        data['old_password'] = test_password

    resp = api_client.post(url, data)

    assert resp.status_code == 400
    assert error_field in resp.data

import pytest

from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from users.models import User


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
    api_client.credentials(HTTP_AUTHORIZATION='Token INVALID_TOKEN')

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

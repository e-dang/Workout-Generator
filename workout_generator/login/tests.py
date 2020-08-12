import pytest

from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_users_list_no_users(client):
    url = reverse('user-list')

    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.data == []


@pytest.mark.django_db
def test_users_list_with_users(client, create_user):
    _ = create_user(username='test_user')
    url = reverse('user-list')

    resp = client.get(url)

    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert resp.data[0]['username'] == 'test_user'


@pytest.mark.django_db
def test_users_detail(client, create_user):
    user = create_user(username='test_user')
    url = reverse('user-detail', kwargs={'pk': user.pk})

    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.data['username'] == 'test_user'


@pytest.mark.django_db
def test_create_user(client):
    url = reverse('user-list')
    user = {
        'username': 'test_user',
        'password': 'test_password',
        'first_name': 'test',
        'last_name': 'demo',
        'email': 'test@demo.com'
    }

    resp = client.post(url, data=user)
    returned_data = resp.data
    returned_data.pop('url')
    returned_data.pop('id')

    assert resp.status_code == 201
    assert user == returned_data


@pytest.mark.django_db
def test_delete_user(client, create_user):
    from django.contrib.auth.models import User
    user = create_user(username='test_user')
    url = reverse('user-detail', kwargs={'pk': user.pk})

    resp = client.delete(url)

    assert resp.status_code == 204
    assert len(User.objects.all()) == 0

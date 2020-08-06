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

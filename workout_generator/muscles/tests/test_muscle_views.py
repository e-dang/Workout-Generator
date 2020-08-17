import pytest

from rest_framework.reverse import reverse
from muscles.models import Muscle


@pytest.mark.django_db
def test_muscle_list(auto_login_user):
    url = reverse('muscle-list')
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert len(resp.data) == len(Muscle.objects.all())


@pytest.mark.django_db
def test_muscle_list_fail_not_logged_in(api_client):
    url = reverse('muscle-list')

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_muscle_detail(auto_login_user):
    muscle_name = 'shoulders'
    url = reverse('muscle-detail', kwargs={'pk': muscle_name})
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert resp.data['name'] == muscle_name


@pytest.mark.django_db
def test_muscle_detail_fail_not_logged_in(api_client):
    muscle_name = 'shoulders'
    url = reverse('muscle-detail', kwargs={'pk': muscle_name})

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_muscle_detail_fail_dne(auto_login_user):
    muscle_name = 'dne'
    url = reverse('muscle-detail', kwargs={'pk': muscle_name})
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 404
    assert 'Not found.' in resp.data['detail']

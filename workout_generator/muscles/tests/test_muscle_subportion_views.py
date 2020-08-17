import pytest

from rest_framework.reverse import reverse
from muscles.models import MuscleSubPortion


@pytest.mark.django_db
def test_muscle_subportions_list(auto_login_user):
    url = reverse('muscle-subportion-list')
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert len(resp.data) == len(MuscleSubPortion.objects.all())


@pytest.mark.django_db
def test_muscle_subportions_list_get_fail_not_logged_in(api_client):
    url = reverse('muscle-subportion-list')

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_muscle_subportions_detail(auto_login_user):
    subportion_name = 'lower traps'
    url = reverse('muscle-subportion-detail', kwargs={'pk': subportion_name})
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert resp.data['name'] == subportion_name


@pytest.mark.django_db
def test_muscle_subportions_detail_fail_not_logged_in(api_client):
    subportion_name = 'lower traps'
    url = reverse('muscle-subportion-detail', kwargs={'pk': subportion_name})

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_muscle_subportions_detail_fail_subportion_dne(auto_login_user):
    subportion_name = 'dne'
    url = reverse('muscle-subportion-detail', kwargs={'pk': subportion_name})
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 404
    assert 'Not found.' in resp.data['detail']

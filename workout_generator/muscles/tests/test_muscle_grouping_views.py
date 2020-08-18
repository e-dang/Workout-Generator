import pytest

from rest_framework.reverse import reverse
from muscles.models import MuscleGrouping


@pytest.mark.django_db
def test_muscle_grouping_list(auto_login_user):
    url = reverse('muscle-grouping-list')
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert len(resp.data) == len(MuscleGrouping.objects.all())


@pytest.mark.django_db
def test_muscle_grouping_list_get_fail_not_logged_in(api_client):
    url = reverse('muscle-grouping-list')

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.parametrize('auto_login_user, grouping_name', [
    (None, 'back'),
    (None, 'shoulders')
], indirect=['auto_login_user'], ids=['not a muscle', 'is a muscle'])
@pytest.mark.django_db
def test_muscle_grouping_detail(auto_login_user, grouping_name):
    url = reverse('muscle-grouping-detail', kwargs={'pk': grouping_name})
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert resp.data['name'] == grouping_name


@pytest.mark.django_db
def test_muscle_grouping_detail_fail_not_logged_in(api_client):
    grouping_name = 'back'
    url = reverse('muscle-grouping-detail', kwargs={'pk': grouping_name})

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_muscle_subportions_detail_fail_subportion_dne(auto_login_user):
    grouping_name = 'dne'
    url = reverse('muscle-grouping-detail', kwargs={'pk': grouping_name})
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 404
    assert 'Not found.' in resp.data['detail']

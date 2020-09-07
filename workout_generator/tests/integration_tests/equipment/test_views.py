import pytest

from rest_framework.reverse import reverse
from equipment.models import Equipment
from rest_framework.test import APIRequestFactory


def get_ids(objs):
    return [obj.id for obj in objs]


@pytest.fixture
def auto_login_profile(auto_login_profile):
    def _auto_login_profile(*args, **kwargs):
        return auto_login_profile(equipment=kwargs.pop('equipment', 4), **kwargs)
    return _auto_login_profile


@pytest.mark.django_db
def test_equipment_list(auto_login_profile):
    url = reverse('equipment-list')
    api_client, _ = auto_login_profile(user__admin=True)

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert len(resp.data) == len(Equipment.objects.all())


@pytest.mark.django_db
def test_equipment_list_fail_not_admin(auto_login_profile):
    url = reverse('equipment-list')
    api_client, _ = auto_login_profile()

    resp = api_client.get(url)

    assert resp.status_code == 403


@pytest.mark.django_db
def test_equipment_list_fail_not_logged_in(api_client):
    url = reverse('equipment-list')

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_equipment_detail(auto_login_profile):
    api_client, profile = auto_login_profile()
    equipment = profile.equipments.last()
    url = reverse('equipment-detail', kwargs={'pk': equipment.id})
    request = APIRequestFactory().get(url)

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert resp.data['owner'] == reverse('profile-detail', kwargs={'pk': profile.id}, request=request)
    assert resp.data['name'] == equipment.name
    assert resp.data['snames'] == equipment.snames


@pytest.mark.django_db
def test_equipment_detail_admin(auto_login_profile):
    _, profile = auto_login_profile()
    api_client, _ = auto_login_profile(user__admin=True)
    equipment = profile.equipments.last()
    url = reverse('equipment-detail', kwargs={'pk': equipment.id})
    request = APIRequestFactory().get(url)

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert resp.data['owner'] == reverse('profile-detail', kwargs={'pk': profile.id}, request=request)
    assert resp.data['name'] == equipment.name
    assert resp.data['snames'] == equipment.snames


@pytest.mark.django_db
def test_equipment_detail_fail_not_owner(auto_login_profile):
    _, profile = auto_login_profile()
    api_client, _ = auto_login_profile()
    equipment = profile.equipments.last()
    url = reverse('equipment-detail', kwargs={'pk': equipment.id})

    resp = api_client.get(url)

    assert resp.status_code == 403


@pytest.mark.django_db
def test_equipment_detail_fail_not_logged_in(auto_login_profile):
    api_client, profile = auto_login_profile()
    api_client.credentials()
    equipment = profile.equipments.last()
    url = reverse('equipment-detail', kwargs={'pk': equipment.id})

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_equipment_detail_delete(auto_login_profile):
    api_client, profile = auto_login_profile()
    num_pieces_before = profile.equipments.count()
    equipment_id = profile.equipments.last().id
    url = reverse('equipment-detail', kwargs={'pk': equipment_id})

    resp = api_client.delete(url)

    assert resp.status_code == 204
    assert profile.equipments.count() == num_pieces_before - 1
    assert not profile.equipments.filter(pk=equipment_id).exists()


@pytest.mark.django_db
def test_user_equipment_list(auto_login_profile):
    _, profile1 = auto_login_profile()
    api_client, profile2 = auto_login_profile()
    equipment1_ids = get_ids(profile1.equipments.all())
    equipment2_ids = get_ids(profile2.equipments.all())
    url = reverse('user-equipment-list', kwargs={'pk': profile2.user.id})

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert len(profile2.equipments.all()) == len(resp.data)
    for obj in resp.data:
        assert obj['id'] in equipment2_ids
        assert obj['id'] not in equipment1_ids


@pytest.mark.django_db
def test_user_equipment_list_admin(auto_login_profile):
    _, profile1 = auto_login_profile()
    api_client, profile2 = auto_login_profile(user__admin=True)
    equipment1_ids = get_ids(profile1.equipments.all())
    equipment2_ids = get_ids(profile2.equipments.all())
    url = reverse('user-equipment-list', kwargs={'pk': profile1.user.id})

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert len(profile1.equipments.all()) == len(resp.data)
    for obj in resp.data:
        assert obj['id'] in equipment1_ids
        assert obj['id'] not in equipment2_ids


@pytest.mark.django_db
def test_user_equipment_list_fail_not_owner(auto_login_profile):
    _, profile1 = auto_login_profile()
    api_client, _ = auto_login_profile()
    url = reverse('user-equipment-list', kwargs={'pk': profile1.user.id})

    resp = api_client.get(url)

    assert resp.status_code == 403


@pytest.mark.django_db
def test_user_equipment_list_fail_not_logged_in(auto_login_profile):
    api_client, profile = auto_login_profile()
    api_client.credentials()
    url = reverse('user-equipment-list', kwargs={'pk': profile.user.id})

    resp = api_client.get(url)

    assert resp.status_code == 401

from rest_framework.reverse import reverse
from tests.unit_tests.conftest import add_api_prefix


def test_equipment_list_url():
    assert reverse('equipment-list') == add_api_prefix('equipment/')


def test_equipment_detail_url():
    pk = 1
    assert reverse('equipment-detail', kwargs={'pk': pk}) == add_api_prefix(f'equipment/{pk}/')


def test_user_equipment_list_url():
    pk = 1
    assert reverse('user-equipment-list', kwargs={'pk': pk}) == add_api_prefix(f'profiles/{pk}/equipment/')

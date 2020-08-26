from rest_framework.reverse import reverse
from tests.unit_tests.conftest import add_api_prefix


def test_muscle_subportion_list_url():
    assert reverse('muscle-subportion-list') == add_api_prefix('muscles/subportion/')


def test_muscle_subportion_detail_url():
    pk = 'lower traps'
    assert reverse('muscle-subportion-detail', kwargs={'pk': pk}) == add_api_prefix(f'muscles/subportion/{pk}/')


def test_muscle_list_url():
    assert reverse('muscle-list') == add_api_prefix('muscles/muscle/')


def test_muscle_detail_url():
    pk = 'lower traps'
    assert reverse('muscle-detail', kwargs={'pk': pk}) == add_api_prefix(f'muscles/muscle/{pk}/')


def test_muscle_grouping_list():
    assert reverse('muscle-grouping-list') == add_api_prefix('muscles/grouping/')


def test_muscle_grouping_detail():
    pk = 'lower traps'
    assert reverse('muscle-grouping-detail', kwargs={'pk': pk}) == add_api_prefix(f'muscles/grouping/{pk}/')

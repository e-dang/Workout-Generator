from rest_framework.reverse import reverse
from tests.unit_tests.conftest import add_api_prefix


def test_user_profile_detail_url():
    pk = 1
    assert reverse('profile-detail', kwargs={'pk': pk}) == add_api_prefix(f'profiles/{pk}/')

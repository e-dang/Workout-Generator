import pytest

from rest_framework.reverse import reverse
from equipment.models import Equipment


@pytest.mark.django_db
def test_equipment_list(auto_login_user):
    url = reverse('equipment-list')
    api_client, _ = auto_login_user()

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert len(resp.data) == len(Equipment.objects.all())

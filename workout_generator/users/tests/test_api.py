import pytest

from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_login(client, create_user, test_password):
    url = reverse('rest_login')
    user = create_user()

    resp = client.post(url, {'email': user.email, 'password': test_password})

    assert resp.status_code == 200
    assert len(resp.data) == 1
    assert 'key' in resp.data
    assert len(resp.data['key']) == 40

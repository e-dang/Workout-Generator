import pytest

from rest_framework.reverse import reverse

pytestmark = pytest.mark.usefixtures('global_user')


@pytest.mark.django_db
def test_user_profile_detail(auto_login_profile):
    api_client, profile = auto_login_profile()
    url = reverse('profile-detail', kwargs={'pk': profile.id})

    resp = api_client.get(url)

    assert resp.status_code == 200
    assert resp.data['weight'] == profile.weight
    assert resp.data['height'] == profile.height
    assert resp.data['bmi'] == profile.bmi
    assert resp.data['visibility'] == profile.visibility


@pytest.mark.django_db
def test_user_profile_detail_fail_wrong_user(auto_login_profile):
    _, profile1 = auto_login_profile()
    api_client, _ = auto_login_profile(email='JaneDoe@demo.com')
    url = reverse('profile-detail', kwargs={'pk': profile1.id})

    resp = api_client.get(url)

    assert resp.status_code == 403


@pytest.mark.django_db
def test_user_profile_detail_fail_not_logged_in(auto_login_profile):
    api_client, profile1 = auto_login_profile()
    api_client.credentials()
    url = reverse('profile-detail', kwargs={'pk': profile1.id})

    resp = api_client.get(url)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_user_profile_update(auto_login_profile):
    api_client, profile = auto_login_profile()
    url = reverse('profile-detail', kwargs={'pk': profile.id})
    new_data = {'weight': 100, 'height': 61, 'bmi': 10, 'visibility': 'pub'}

    resp = api_client.patch(url, data=new_data)

    assert resp.status_code == 200
    assert resp.data['weight'] == new_data['weight']
    assert resp.data['height'] == new_data['height']
    assert resp.data['bmi'] == new_data['bmi']
    assert resp.data['visibility'] == new_data['visibility']
    assert resp.data['weight'] != profile.weight
    assert resp.data['height'] != profile.height
    assert resp.data['bmi'] != profile.bmi
    assert resp.data['visibility'] != profile.visibility


@pytest.mark.parametrize('auto_login_profile, new_data, error_attr, error_code', [
    (None, {'weight': 100000, 'height': 61, 'bmi': 10, 'visibility': 'pub'}, 'weight', 'max_value'),
    (None, {'weight': 100, 'height': 100000, 'bmi': 10, 'visibility': 'pub'}, 'height', 'max_value'),
    (None, {'weight': 100, 'height': 61, 'bmi': 100000, 'visibility': 'pub'}, 'bmi', 'max_value'),
    (None, {'weight': 100, 'height': 61, 'bmi': 10, 'visibility': 'dne'}, 'visibility', 'invalid_choice')
],
    indirect=['auto_login_profile'],
    ids=['invalid weight', 'invalid height', 'invalid bmi', 'invalid visibility'])
@pytest.mark.django_db
def test_user_profile_update_fail_invalid_data(auto_login_profile, new_data, error_attr, error_code):
    api_client, profile = auto_login_profile()
    url = reverse('profile-detail', kwargs={'pk': profile.id})

    resp = api_client.patch(url, data=new_data)

    assert resp.status_code == 400
    assert resp.data[error_attr][0].code == error_code


def test_user_profile_update_fail_wrong_user(auto_login_profile):
    _, profile = auto_login_profile()
    api_client, _ = auto_login_profile(email='JaneDoe@demo.com')
    url = reverse('profile-detail', kwargs={'pk': profile.id})
    new_data = {'weight': 100, 'height': 61, 'bmi': 10, 'visibility': 'pub'}

    resp = api_client.patch(url, data=new_data)

    assert resp.status_code == 403


def test_user_profile_update_fail_not_logged_in(auto_login_profile):
    api_client, profile = auto_login_profile()
    api_client.credentials()
    url = reverse('profile-detail', kwargs={'pk': profile.id})
    new_data = {'weight': 100, 'height': 61, 'bmi': 10, 'visibility': 'pub'}

    resp = api_client.patch(url, data=new_data)

    assert resp.status_code == 401

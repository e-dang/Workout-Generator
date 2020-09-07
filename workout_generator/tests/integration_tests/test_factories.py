import pytest

from user_profiles.models import UserProfile, Following, FollowRequest
from users.models import User
from equipment.models import Equipment


@pytest.mark.parametrize('auto_create_user_factory, status, expected', [
    (None, {}, {'is_active': True, 'is_staff': False, 'is_superuser': False}),
    (None, {'inactive': True}, {'is_active': False, 'is_staff': False, 'is_superuser': False}),
    (None, {'active': True}, {'is_active': True, 'is_staff': False, 'is_superuser': False}),
    (None, {'staff': True}, {'is_active': True, 'is_staff': True, 'is_superuser': False}),
    (None, {'admin': True}, {'is_active': True, 'is_staff': True, 'is_superuser': True})
],
    indirect=['auto_create_user_factory'],
    ids=['default', 'inactive', 'active', 'staff', 'admin'])
@pytest.mark.django_db
def test_auto_create_user_factory(auto_create_user_factory, status, expected):
    user = auto_create_user_factory(**status)

    assert isinstance(user, User)
    assert user == user.profile.user
    for key, value in expected.items():
        assert getattr(user, key) == value


@pytest.mark.parametrize('followers', [0, 2], ids=['0', '2'])
@pytest.mark.parametrize('follower_requests', [0, 2], ids=['0', '2'])
@pytest.mark.parametrize('equipment', [0, 2], ids=['0', '2'])
@pytest.mark.parametrize('user_profile_factory', [None],
                         indirect=['user_profile_factory'])
@pytest.mark.django_db
def test_profile_factory(user_profile_factory, followers, follower_requests, equipment):
    profile = user_profile_factory(followers=followers, follower_requests=follower_requests, equipment=equipment)

    num_profiles = 1 + followers + follower_requests + equipment
    assert isinstance(profile, UserProfile)
    assert profile == profile.user.profile
    assert len(profile.following.all()) == followers
    assert len(profile.following_requests.all()) == follower_requests
    assert len(profile.equipments.all()) == equipment
    assert len(User.objects.all()) == num_profiles
    assert len(UserProfile.objects.all()) == num_profiles
    assert len(Following.objects.all()) == followers
    assert len(FollowRequest.objects.all()) == follower_requests
    assert len(Equipment.objects.all()) == equipment


@pytest.mark.django_db
def test_following_factory(following_factory):
    following = following_factory()

    assert isinstance(following, Following)
    assert isinstance(following.following_user, UserProfile)
    assert isinstance(following.followed_user, UserProfile)
    assert following.following_user != following.followed_user


@pytest.mark.django_db
def test_follow_request_factory(follow_request_factory):
    follow_request = follow_request_factory()

    assert isinstance(follow_request, FollowRequest)
    assert isinstance(follow_request.requesting_profile, UserProfile)
    assert isinstance(follow_request.target_profile, UserProfile)
    assert follow_request.requesting_profile != follow_request.target_profile


@pytest.mark.django_db
def test_equipment_factory(equipment_factory):
    equipment = equipment_factory()

    assert isinstance(equipment, Equipment)
    assert isinstance(equipment.owner, UserProfile)

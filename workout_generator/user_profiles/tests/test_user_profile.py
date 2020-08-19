import pytest
import os

from user_profiles.models import UserProfile, Following, FollowRequest


@pytest.mark.django_db
def test_follow_profile(create_user):
    """
    Tests that the instance method _follow_profile() correctly places the profiles in the following field of each
    profile.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    profile1 = user1.profile
    profile2 = user2.profile

    profile1._follow_profile(profile2)

    assert profile2 in profile1.following.all()
    assert profile2 not in profile1.followers.all()
    assert profile1 not in profile2.following.all()
    assert profile1 in profile2.followers.all()


@pytest.mark.django_db
def test_accept_follower_request(create_user):
    """
    Tests that the instance method _accept_follower_request() correctly places the profiles in the following field of
    each profile.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    profile1 = user1.profile
    profile2 = user2.profile
    follower_request = FollowRequest.objects.create(requesting_profile=profile2, target_profile=profile1)

    profile1._accept_follower_request(follower_request)

    assert profile2 in profile1.followers.all()
    assert profile2 not in profile1.following.all()
    assert profile1 in profile2.following.all()
    assert profile1 not in profile2.followers.all()


@pytest.mark.django_db
def test_accept_follower_request_fail(create_user):
    """
    Tests that the instance method _accept_follower_request() does not change anything if the target_profile on the
    FollowRequest is not the same as the profile that issued the request.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    profile1 = user1.profile
    profile2 = user2.profile
    follower_request = FollowRequest.objects.create(requesting_profile=profile1, target_profile=profile2)

    profile1._accept_follower_request(follower_request)

    assert profile2 not in profile1.followers.all()
    assert profile2 not in profile1.following.all()
    assert profile1 not in profile2.following.all()
    assert profile1 not in profile2.followers.all()


@pytest.mark.django_db
def test_user_profile_auto_create(create_user):
    """
    Tests that when a new User is created that it automatically follows the global User instance.
    """

    user = create_user()

    profile = UserProfile.objects.get(user=user.id)

    global_user = UserProfile.objects.get(user__email=os.environ.get('GLOBAL_EMAIL'))
    followers = global_user.followers.all()
    assert user.profile == profile
    assert len(profile.following.all()) == 1
    assert len(profile.followers.all()) == 0
    assert len(followers) == 2
    assert profile in followers


@pytest.mark.django_db
def test_user_profile_deleted_on_user_delete(create_user):
    """
    Tests that when a User is deleted so is their associated UserProfile, Following entries, and FollowRequests.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    FollowRequest.objects.create(requesting_profile=user1.profile, target_profile=user2.profile)
    user_profile_before = len(UserProfile.objects.all())
    following_before = len(Following.objects.all())
    follow_request_before = len(FollowRequest.objects.all())

    user1.delete()

    assert len(UserProfile.objects.all()) == user_profile_before - 1
    assert len(Following.objects.all()) == following_before - 1
    assert len(FollowRequest.objects.all()) == follow_request_before - 1

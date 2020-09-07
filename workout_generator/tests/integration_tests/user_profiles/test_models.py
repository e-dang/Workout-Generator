import pytest
import os

from user_profiles.models import UserProfile, Following, FollowRequest
from django.db.utils import IntegrityError
from user_profiles.exceptions import InvalidFollowRequest


@pytest.mark.django_db
def test_make_follow_request_public(user_profile_factory):
    """
    Tests that the instance method make_follow_request() correctly places the profiles in the following field of each
    profile when the followed User has public visibility.
    """

    profile1 = user_profile_factory()
    profile2 = user_profile_factory(visibility=UserProfile.PUBLIC)

    profile1.make_follow_request(profile2)

    assert profile2 in profile1.following.all()
    assert profile2 not in profile1.followers.all()
    assert profile1 not in profile2.following.all()
    assert profile1 in profile2.followers.all()


@pytest.mark.django_db
def test_make_follow_request_private(user_profile_factory):
    """
    Tests that the instance method make_follow_request() correctly issues a FollowRequest when the followed User has
    private visibility.
    """

    profile1 = user_profile_factory()
    profile2 = user_profile_factory(visibility=UserProfile.PRIVATE)

    profile1.make_follow_request(profile2)

    assert profile2 not in profile1.following.all()
    assert profile2 not in profile1.followers.all()
    assert profile1 not in profile2.following.all()
    assert profile1 not in profile2.followers.all()
    assert profile1 in profile2.follower_requests.all()
    assert profile1 not in profile2.following_requests.all()
    assert profile2 in profile1.following_requests.all()
    assert profile2 not in profile1.follower_requests.all()


@pytest.mark.parametrize('user_profile_factory, accepted', [
    (None, True),
    (None, False)
],
    indirect=['user_profile_factory'],
    ids=['accepted', 'not accepted'])
@pytest.mark.django_db
def test_handle_follow_request(user_profile_factory, accepted):
    """
    Tests that the instance method handle_follower_request() correctly places the profiles in the following field of
    each profile when the request has been accepted, does nothing when the request has been rejected, and deletes
    the request in either case.
    """

    profile1 = user_profile_factory()
    profile2 = user_profile_factory()
    follower_request = FollowRequest.objects.create(requesting_profile=profile2, target_profile=profile1)

    profile1.handle_follow_request(follower_request, accepted)

    if accepted:
        assert profile2 in profile1.followers.all()
        assert profile2 not in profile1.following.all()
        assert profile1 in profile2.following.all()
        assert profile1 not in profile2.followers.all()
    else:
        assert profile2 not in profile1.followers.all()
        assert profile2 not in profile1.following.all()
        assert profile1 not in profile2.following.all()
        assert profile1 not in profile2.followers.all()

    assert len(FollowRequest.objects.all()) == 0


@pytest.mark.parametrize('user_profile_factory, accepted', [
    (None, True),
    (None, False)
],
    indirect=['user_profile_factory'],
    ids=['accepted', 'not accepted'])
@pytest.mark.django_db
def test_handle_follow_request_invalid_request(user_profile_factory, accepted):
    """
    Tests that the instance method handle_follower_request() does nothing when a follower_request not belonging to the
    calling instance is passed to method.
    """

    profile1 = user_profile_factory()
    profile2 = user_profile_factory()
    follower_request = FollowRequest.objects.create(requesting_profile=profile1, target_profile=profile2)

    with pytest.raises(InvalidFollowRequest):
        profile1.handle_follow_request(follower_request, accepted)

    assert profile2 not in profile1.followers.all()
    assert profile2 not in profile1.following.all()
    assert profile1 not in profile2.following.all()
    assert profile1 not in profile2.followers.all()
    assert len(FollowRequest.objects.all()) == 1


@pytest.mark.django_db
def test_user_profile_deleted_on_user_delete(user_profile_factory):
    """
    Tests that when a User is deleted so is their associated UserProfile, Following entries, and FollowRequests.
    """

    profile1 = user_profile_factory()
    profile2 = user_profile_factory()
    profile3 = user_profile_factory()
    profile1.followers.add(profile3)
    profile3.following.add(profile1)
    FollowRequest.objects.create(requesting_profile=profile1, target_profile=profile2)
    user_profile_before = len(UserProfile.objects.all())
    follow_request_before = len(FollowRequest.objects.all())

    profile1.user.delete()

    assert len(UserProfile.objects.all()) == user_profile_before - 1
    assert len(Following.objects.all()) == 0
    assert len(FollowRequest.objects.all()) == follow_request_before - 1


@pytest.mark.django_db
def test_unique_together_constraint_following(user_profile_factory):
    profile1 = user_profile_factory()
    profile2 = user_profile_factory()
    Following.objects.create(following_user=profile1, followed_user=profile2)

    with pytest.raises(IntegrityError):
        Following.objects.create(following_user=profile1, followed_user=profile2)


@pytest.mark.django_db
def test_unique_together_constraint_follow_request(user_profile_factory):
    profile1 = user_profile_factory()
    profile2 = user_profile_factory()
    FollowRequest.objects.create(requesting_profile=profile1, target_profile=profile2)

    with pytest.raises(IntegrityError):
        FollowRequest.objects.create(requesting_profile=profile1, target_profile=profile2)


# @pytest.mark.django_db
# def test_user_profile_auto_create(global_user, user_profile_factory):
#     """
#     Tests that when a new User is created that it automatically follows the global User instance.
#     """

#     user = user_profile_factory()

#     profile = UserProfile.objects.get(user=user.id)

#     global_user = UserProfile.objects.get(user__email=os.environ.get('GLOBAL_EMAIL'))
#     followers = global_user.followers.all()
#     assert user.profile == profile
#     assert len(profile.following.all()) == 1
#     assert len(profile.followers.all()) == 0
#     assert len(followers) == 2
#     assert profile in followers

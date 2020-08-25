import pytest

from user_profiles.models import UserProfile, Following, FollowRequest
from django.db.utils import IntegrityError
from user_profiles.exceptions import InvalidFollowRequest


@pytest.mark.django_db
def test_make_follow_request_public(create_user):
    """
    Tests that the instance method make_follow_request() correctly places the profiles in the following field of each
    profile when the followed User has public visibility.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com', visibility=UserProfile.PUBLIC)
    profile1 = user1.profile
    profile2 = user2.profile

    profile1.make_follow_request(profile2)

    assert profile2 in profile1.following.all()
    assert profile2 not in profile1.followers.all()
    assert profile1 not in profile2.following.all()
    assert profile1 in profile2.followers.all()


@pytest.mark.django_db
def test_make_follow_request_private(create_user):
    """
    Tests that the instance method make_follow_request() correctly issues a FollowRequest when the followed User has
    private visibility.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    profile1 = user1.profile
    profile2 = user2.profile

    profile1.make_follow_request(profile2)

    assert profile2 not in profile1.following.all()
    assert profile2 not in profile1.followers.all()
    assert profile1 not in profile2.following.all()
    assert profile1 not in profile2.followers.all()
    assert profile1 in profile2.follower_requests.all()
    assert profile1 not in profile2.following_requests.all()
    assert profile2 in profile1.following_requests.all()
    assert profile2 not in profile1.follower_requests.all()


@pytest.mark.parametrize('create_user, accepted', [
    (None, True),
    (None, False)
],
    indirect=['create_user'],
    ids=['accepted', 'not accepted'])
@pytest.mark.django_db
def test_handle_follow_request(create_user, accepted):
    """
    Tests that the instance method handle_follower_request() correctly places the profiles in the following field of
    each profile when the request has been accepted, does nothing when the request has been rejected, and deletes
    the request in either case.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    profile1 = user1.profile
    profile2 = user2.profile
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


@pytest.mark.parametrize('create_user, accepted', [
    (None, True),
    (None, False)
],
    indirect=['create_user'],
    ids=['accepted', 'not accepted'])
@pytest.mark.django_db
def test_handle_follow_request_invalid_request(create_user, accepted):
    """
    Tests that the instance method handle_follower_request() does nothing when a follower_request not belonging to the
    calling instance is passed to method.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    profile1 = user1.profile
    profile2 = user2.profile
    follower_request = FollowRequest.objects.create(requesting_profile=profile1, target_profile=profile2)

    with pytest.raises(InvalidFollowRequest):
        profile1.handle_follow_request(follower_request, accepted)

    assert profile2 not in profile1.followers.all()
    assert profile2 not in profile1.following.all()
    assert profile1 not in profile2.following.all()
    assert profile1 not in profile2.followers.all()
    assert len(FollowRequest.objects.all()) == 1


@pytest.mark.django_db
def test_user_profile_deleted_on_user_delete(create_user):
    """
    Tests that when a User is deleted so is their associated UserProfile, Following entries, and FollowRequests.
    """

    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    user3 = create_user(email='test@demo.com')
    user1.profile.followers.add(user3.profile)
    user3.profile.following.add(user1.profile)
    FollowRequest.objects.create(requesting_profile=user1.profile, target_profile=user2.profile)
    user_profile_before = len(UserProfile.objects.all())
    follow_request_before = len(FollowRequest.objects.all())

    user1.delete()

    assert len(UserProfile.objects.all()) == user_profile_before - 1
    assert len(Following.objects.all()) == 0
    assert len(FollowRequest.objects.all()) == follow_request_before - 1


@pytest.mark.django_db
def test_unique_together_constraint_following(create_user):
    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    Following.objects.create(following_user=user1.profile, followed_user=user2.profile)

    with pytest.raises(IntegrityError):
        Following.objects.create(following_user=user1.profile, followed_user=user2.profile)


@pytest.mark.django_db
def test_unique_together_constraint_follow_request(create_user):
    user1 = create_user()
    user2 = create_user(email='JaneDoe@demo.com')
    FollowRequest.objects.create(requesting_profile=user1.profile, target_profile=user2.profile)

    with pytest.raises(IntegrityError):
        FollowRequest.objects.create(requesting_profile=user1.profile, target_profile=user2.profile)

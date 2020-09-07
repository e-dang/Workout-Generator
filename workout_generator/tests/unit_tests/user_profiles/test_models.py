import pytest
import mock
from user_profiles.models import UserProfile, FollowRequest, Following
from users.models import User
from user_profiles.exceptions import InvalidFollowRequest


def test_user_profile_str():
    mock_user = mock.MagicMock(spec=User)
    mock_user.__str__.return_value = 'JohnDoe@demo.com'
    mock_profile = mock.MagicMock(spec=UserProfile)
    mock_profile.user = mock_user

    assert UserProfile.__str__(mock_profile) == 'JohnDoe@demo.com'


def test_user_profile_make_follow_request_public():
    mock_profile1 = mock.MagicMock(spec=UserProfile)
    mock_profile2 = mock.MagicMock(spec=UserProfile)
    mock_profile1.PUBLIC = UserProfile.PUBLIC
    mock_profile2.visibility = UserProfile.PUBLIC

    with mock.patch('user_profiles.models.Following') as mock_following:
        UserProfile.make_follow_request(mock_profile1, mock_profile2)

        mock_following.objects.create.assert_called_once_with(following_user=mock_profile1, followed_user=mock_profile2)


def test_user_profile_make_follow_request_private():
    mock_profile1 = mock.MagicMock(spec=UserProfile)
    mock_profile2 = mock.MagicMock(spec=UserProfile)
    mock_profile1.PRIVATE = UserProfile.PRIVATE
    mock_profile2.visibility = UserProfile.PRIVATE

    with mock.patch('user_profiles.models.FollowRequest') as mock_follow_request:
        UserProfile.make_follow_request(mock_profile1, mock_profile2)

        mock_follow_request.objects.create.assert_called_once_with(
            requesting_profile=mock_profile1, target_profile=mock_profile2)


def test_user_profile_handle_follow_request_accepted():
    mock_profile1 = mock.MagicMock(spec=UserProfile)
    mock_profile2 = mock.MagicMock(spec=UserProfile)
    mock_follow_request = mock.MagicMock(spec=FollowRequest)
    mock_follow_request.requesting_profile = mock_profile1
    mock_follow_request.target_profile = mock_profile2

    with mock.patch('user_profiles.models.Following') as mock_following:
        UserProfile.handle_follow_request(mock_profile2, mock_follow_request, True)

        mock_following.objects.create.assert_called_once_with(following_user=mock_profile1, followed_user=mock_profile2)
        mock_follow_request.delete.assert_called_once()


def test_user_profile_handle_follow_request_not_accepted():
    mock_profile1 = mock.MagicMock(spec=UserProfile)
    mock_profile2 = mock.MagicMock(spec=UserProfile)
    mock_follow_request = mock.MagicMock(spec=FollowRequest)
    mock_follow_request.requesting_profile = mock_profile1
    mock_follow_request.target_profile = mock_profile2

    with mock.patch('user_profiles.models.Following') as mock_following:
        UserProfile.handle_follow_request(mock_profile2, mock_follow_request, False)

        mock_following.objects.create.assert_not_called()
        mock_follow_request.delete.assert_called_once()


@pytest.mark.parametrize('accepted', [
    True,
    False
],
    ids=['accepted', 'not accepted'])
def test_user_profile_handle_follow_request_invalid_request(accepted):
    mock_profile1 = mock.MagicMock(spec=UserProfile)
    mock_profile2 = mock.MagicMock(spec=UserProfile)
    mock_follow_request = mock.MagicMock(spec=FollowRequest)
    mock_follow_request.requesting_profile = mock_profile2
    mock_follow_request.target_profile = mock_profile1

    with pytest.raises(InvalidFollowRequest):
        UserProfile.handle_follow_request(mock_profile2, mock_follow_request, accepted)


def test_following_str():
    email1 = 'JohnDoe@demo.com'
    email2 = 'JaneDoe@demo.com'
    mock_following = mock.MagicMock(spec=Following)
    mock_following.following_user.user.__str__.return_value = email1
    mock_following.followed_user.user.__str__.return_value = email2

    assert Following.__str__(mock_following) == f'{email1} follows {email2}'


def test_follow_request_str():
    email1 = 'JohnDoe@demo.com'
    email2 = 'JaneDoe@demo.com'
    mock_follow_request = mock.MagicMock(spec=FollowRequest)
    mock_follow_request.requesting_profile.user.__str__.return_value = email1
    mock_follow_request.target_profile.user.__str__.return_value = email2

    assert FollowRequest.__str__(mock_follow_request) == f'{email1} is requesting to follow {email2}'

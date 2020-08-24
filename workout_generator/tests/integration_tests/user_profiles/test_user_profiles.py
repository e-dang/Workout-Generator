import os

import pytest

from user_profiles.models import UserProfile


@pytest.mark.django_db
def test_user_profile_auto_create(global_user, create_user):
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

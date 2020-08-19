from django.db import models
from users.models import User


class UserProfile(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    UNKNOWN = 'u'
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (UNKNOWN, 'Unspecified')
    )

    PRIVATE = 'pri'
    PUBLIC = 'pub'
    PRIVACY = (
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public')
    )

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS, default=UNKNOWN)
    weight = models.SmallIntegerField(default=-1)
    height = models.SmallIntegerField(default=-1)
    bmi = models.SmallIntegerField(default=-1)
    visibility = models.CharField(max_length=3, choices=PRIVACY, default=PRIVATE)
    following = models.ManyToManyField(
        'self', related_name='followers', through='Following', symmetrical=False)
    following_requests = models.ManyToManyField(
        'self', related_name='follower_requests', through='FollowRequest', symmetrical=False)

    def make_follow_request(self, user_profile):
        if user_profile.visibility == self.PUBLIC:
            self._follow_profile(user_profile)
        else:
            self._issue_follow_request(user_profile)

    def handle_follow_request(self, user_profile, accepted):
        try:
            follower_request = self.follower_requests.get(requesting_profile=user_profile, target_profile=self)
        except self.following_requests.model.DoesNotExist:
            pass
        else:
            if accepted:
                self._accept_follower_request(follower_request)

            follower_request.delete()

    def _follow_profile(self, user_profile):
        self.following.add(user_profile)
        user_profile.followers.add(self)

    def _issue_follow_request(self, user_profile):
        self.following_requests.add(user_profile)
        user_profile.follower_requests.add(self)

    def _accept_follower_request(self, follower_request):
        if follower_request.target_profile == self:
            user_profile = follower_request.requesting_profile
            self.followers.add(user_profile)
            user_profile.following.add(self)

    def __str__(self):
        return str(self.user)

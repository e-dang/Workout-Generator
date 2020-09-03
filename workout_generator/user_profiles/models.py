from django.db import models
from users.models import User
from user_profiles.exceptions import InvalidFollowRequest
from content_subscriptions.models import SubscriptionHolderAddons


class UserProfile(SubscriptionHolderAddons, models.Model):
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
            Following.objects.create(following_user=self, followed_user=user_profile)
        else:
            FollowRequest.objects.create(requesting_profile=self, target_profile=user_profile)

    def handle_follow_request(self, follower_request, accepted):
        if follower_request.target_profile != self:
            raise InvalidFollowRequest('The given FollowRequest does not belong to this UserProfile!')

        if accepted:
            Following.objects.create(following_user=follower_request.requesting_profile, followed_user=self)

        follower_request.delete()

    def __str__(self):
        return str(self.user)


class Following(models.Model):
    following_user = models.ForeignKey(UserProfile, related_name='following_user', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(UserProfile, related_name='followed_user', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('following_user', 'followed_user')
        ordering = ('-created', )

    def __str__(self):
        return f'{str(self.following_user.user)} follows {str(self.followed_user.user)}'


class FollowRequest(models.Model):
    requesting_profile = models.ForeignKey(UserProfile, related_name='requesting_profile', on_delete=models.CASCADE)
    target_profile = models.ForeignKey(UserProfile, related_name='target_profile', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('requesting_profile', 'target_profile')
        ordering = ('-created', )

    def __str__(self):
        return f'{str(self.requesting_profile.user)} is requesting to follow {str(self.target_profile.user)}'

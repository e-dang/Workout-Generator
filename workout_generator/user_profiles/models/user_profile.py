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

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS, default=UNKNOWN)
    weight = models.SmallIntegerField(default=-1)
    height = models.SmallIntegerField(default=-1)
    bmi = models.SmallIntegerField(default=-1)
    following = models.ManyToManyField(
        'self', related_name='followers', through='Following', symmetrical=False)

    def follow_user(self, user_profile):
        self.following.add(user_profile)
        user_profile.followers.add(self)

    def __str__(self):
        return str(self.user)

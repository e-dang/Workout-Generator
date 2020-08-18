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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS, default=UNKNOWN)
    weight = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    bmi = models.PositiveSmallIntegerField()
    followers = models.ManyToManyField('self', related_name='followers', through='Followers', symmetrical=False)
    following = models.ManyToManyField('self', related_name='follows', through='Following', symmetrical=False)

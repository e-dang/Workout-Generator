from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


# Taken from https://krakensystems.co/blog/2020/custom-users-using-django-rest-framework
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

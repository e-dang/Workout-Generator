from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Username: {self.username}, Email: {self.email}'

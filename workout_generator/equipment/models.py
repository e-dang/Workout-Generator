from django.db import models
from django.contrib.postgres.fields import ArrayField
from content_subscriptions.models import Subscribable
from content_subscriptions.registry import register


class Equipment(Subscribable):
    name = models.CharField(max_length=25)
    other_names = ArrayField(models.CharField(max_length=25))

    def __str__(self):
        return self.name

    @property
    def aliases(self):
        return [self.name] + self.other_names

    @property
    def user(self):
        return self.owner.user


register(Equipment)

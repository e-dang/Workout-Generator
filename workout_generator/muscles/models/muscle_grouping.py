from django.contrib.postgres.fields import ArrayField
from django.db import models

from .muscle import Muscle


class MuscleGrouping(models.Model):
    """
    This model represents the groupings of muscles either by anatomy, function, or groupings of muscles that are
    commonly exercised together. Furthermore, all Muscles are considered to be a MuscleGrouping containing only one
    Muscle. Thus, all Muscles are MuscleGrouping, but not all MuscleGroupings are Muscles. Some examples of valid
    MuscleGroupings that are not Muscles are legs (anatomy),  push (function), posterior chain (commonly exercised
    together).
    """

    name = models.CharField(max_length=25, primary_key=True)
    other_names = ArrayField(models.CharField(max_length=25))
    muscles = models.ManyToManyField(Muscle)

    def __str__(self):
        return self.name.capitalize()

    @property
    def aliases(self):
        return [self.name] + self.other_names

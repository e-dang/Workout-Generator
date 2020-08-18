from django.contrib.postgres.fields import ArrayField
from django.db import models

from .muscle_subportion import MuscleSubPortion


class Muscle(models.Model):
    """
    This model does not necessarily represent a singular muscle in the formal sense since human anatomy is complex.
    Rather it represents a muscle or muscle group that is either commonly referred to as a singular muscle or is a
    MuscleSubPortion. Thus, all MuscleSubPortions are also considered Muscles, while some Muscles are not
    MuscleSubPortions. Some examples of Muscles that are not MuscleSubPortions are biceps, triceps, quads, and shoulder.
    Some examples that are not considered a muscle in this definition are legs and vastus lateralis (a specific muscle
    in the quads).
    """

    name = models.CharField(max_length=25, primary_key=True)
    other_names = ArrayField(models.CharField(max_length=25))
    subportions = models.ManyToManyField(MuscleSubPortion)

    def __str__(self):
        return self.name.capitalize()

    @property
    def aliases(self):
        return [self.name] + self.other_names

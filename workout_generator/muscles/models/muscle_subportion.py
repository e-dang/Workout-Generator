from django.contrib.postgres.fields import ArrayField
from django.db import models


class MuscleSubPortion(models.Model):
    """
    This model represents a portion of what is commonly referred to as a muscle that can be either targeted
    preferentailly or isolated by a Movement. Some examples of valid MuscleSubPortions are upper chest and front
    shoulder. These are valid MuscleSubPortions because the upper chest can be targeted preferentially over the middle
    and lower chest by doing Movements such as an incline benchpress, and the front shoulder can be isolated from the
    side and rear shoulders by Movements that raise the arm in front of the body. Some examples of invalid
    MuscleSubPortions are shoulder and chest as these would be considered whole muscles rather than a portion of a
    muscle.
    """

    name = models.CharField(max_length=25, primary_key=True)
    other_names = ArrayField(models.CharField(max_length=25))

    def __str__(self):
        return self.name.capitalize()

    @property
    def aliases(self):
        return [self.name] + self.other_names

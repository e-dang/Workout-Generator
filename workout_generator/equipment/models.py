from django.db import models
from django.contrib.postgres.fields import ArrayField

from users.models import User


class Equipment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=25)
    other_names = ArrayField(models.CharField(max_length=25))
    shared_with = models.ManyToManyField(User, through='SharedEquipment', related_name='shared_equipment')

    def __str__(self):
        return self.name

    @property
    def aliases(self):
        return [self.name] + self.other_names


class SharedEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Equipment: {self.equipment}, Reciever: {self.reciever.email}'

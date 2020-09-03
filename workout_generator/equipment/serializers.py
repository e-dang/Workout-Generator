from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Equipment


class ArrayField(serializers.ListField):
    child = serializers.CharField(max_length=25, allow_blank=True)


class EquipmentSerializer(serializers.ModelSerializer):
    other_names = ArrayField()

    class Meta:
        model = Equipment
        fields = ('owner', 'name', 'other_names')
        validators = [UniqueTogetherValidator(Equipment.objects.all(), ('owner', 'name'))]

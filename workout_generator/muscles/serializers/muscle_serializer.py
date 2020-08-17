from rest_framework.serializers import ModelSerializer
from muscles.models import Muscle


class MuscleSerializer(ModelSerializer):
    class Meta:
        model = Muscle
        fields = ('name', 'other_names', 'subportions')

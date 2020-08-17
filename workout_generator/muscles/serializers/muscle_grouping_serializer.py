from rest_framework.serializers import ModelSerializer
from muscles.models import MuscleGrouping


class MuscleGroupingSerializer(ModelSerializer):
    class Meta:
        model = MuscleGrouping
        fields = ('name', 'other_names', 'muscles')

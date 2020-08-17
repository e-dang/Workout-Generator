from rest_framework.serializers import ModelSerializer
from muscles.models import MuscleSubPortion


class MuscleSubPortionSerializer(ModelSerializer):
    class Meta:
        model = MuscleSubPortion
        fields = ('name', 'other_names')

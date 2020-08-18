from rest_framework.generics import ListAPIView, RetrieveAPIView
from muscles.serializers import MuscleSerializer
from muscles.models import Muscle


class MuscleList(ListAPIView):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer


class MuscleDetail(RetrieveAPIView):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer

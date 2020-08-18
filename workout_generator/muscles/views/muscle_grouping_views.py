from rest_framework.generics import ListAPIView, RetrieveAPIView
from muscles.serializers import MuscleGroupingSerializer
from muscles.models import MuscleGrouping


class MuscleGroupingList(ListAPIView):
    queryset = MuscleGrouping.objects.all()
    serializer_class = MuscleGroupingSerializer


class MuscleGroupingDetail(RetrieveAPIView):
    queryset = MuscleGrouping.objects.all()
    serializer_class = MuscleGroupingSerializer

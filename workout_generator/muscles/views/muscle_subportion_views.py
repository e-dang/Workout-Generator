from rest_framework.generics import ListAPIView, RetrieveAPIView
from muscles.serializers import MuscleSubPortionSerializer
from muscles.models import MuscleSubPortion


class MuscleSubPortionList(ListAPIView):
    queryset = MuscleSubPortion.objects.all()
    serializer_class = MuscleSubPortionSerializer


class MuscleSubPortionDetail(RetrieveAPIView):
    queryset = MuscleSubPortion.objects.all()
    serializer_class = MuscleSubPortionSerializer

from common.views import HistoryView
from rest_framework import generics

from ..models.checkins import CheckIn
from ..serializers.checkins import CheckInNestedSerializer, CheckInSerializer


class CheckInListView(generics.ListCreateAPIView):
    queryset = (
        CheckIn.objects.prefetch_related("drugs")
        .prefetch_related("high_interaction_potential_drugs")
        .prefetch_related("diagnoses_drugs")
        .prefetch_related("diagnoses")
        .all()
    )
    serializer_class = CheckInSerializer


class CheckInDetailView(generics.RetrieveUpdateAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CheckInNestedSerializer
        return CheckInSerializer


class CheckInHistoryView(HistoryView):
    queryset = CheckIn.objects.all()

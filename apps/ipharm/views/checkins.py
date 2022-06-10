from common.views import HistoryView
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models.checkins import CheckIn, CheckInDiagnosis
from ..serializers.checkins import (
    CheckInDiagnosisSerializer,
    CheckInNestedSerializer,
    CheckInSerializer,
)


class CheckInListView(generics.ListCreateAPIView):
    queryset = (
        CheckIn.objects.prefetch_related("drugs")
        .prefetch_related("high_interaction_potential_drugs")
        .prefetch_related("narrow_therapeutic_window_drugs")
        .prefetch_related(
            Prefetch(
                "diagnoses", queryset=CheckInDiagnosis.objects.prefetch_related("drugs")
            )
        )
        .all()
    )
    serializer_class = CheckInSerializer


class CheckInDetailView(generics.RetrieveUpdateAPIView):
    queryset = (
        CheckIn.objects.prefetch_related("drugs")
        .prefetch_related("high_interaction_potential_drugs")
        .prefetch_related("narrow_therapeutic_window_drugs")
        .prefetch_related(
            Prefetch(
                "diagnoses", queryset=CheckInDiagnosis.objects.prefetch_related("drugs")
            )
        )
        .all()
    )
    serializer_class = CheckInSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CheckInNestedSerializer
        return CheckInSerializer


class CheckInHistoryView(HistoryView):
    queryset = CheckIn.objects.all()


class CheckInDiagnosisListView(generics.ListCreateAPIView):
    queryset = CheckInDiagnosis.objects.all()
    serializer_class = CheckInDiagnosisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["check_in"]


class CheckInDiagnosisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CheckInDiagnosis.objects.all()
    serializer_class = CheckInDiagnosisSerializer


class CheckInDiagnosisHistoryView(HistoryView):
    queryset = CheckInDiagnosis.objects.all()

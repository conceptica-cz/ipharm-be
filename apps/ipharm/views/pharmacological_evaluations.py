from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models.pharmacological_evaluations import PharmacologicalEvaluation
from ..serializers.pharmacological_evaluations import (
    PharmacologicalEvaluationNestedSerializer,
    PharmacologicalEvaluationSerializer,
)
from .common import HistoryView


class PharmacologicalEvaluationListView(generics.ListCreateAPIView):
    queryset = PharmacologicalEvaluation.objects.all()
    serializer_class = PharmacologicalEvaluationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["care"]


class PharmacologicalEvaluationDetailView(
    generics.RetrieveUpdateAPIView,
):
    queryset = PharmacologicalEvaluation.objects.all()
    serializer_class = PharmacologicalEvaluationSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PharmacologicalEvaluationNestedSerializer
        return PharmacologicalEvaluationSerializer


class PharmacologicalEvaluationHistoryView(HistoryView):
    queryset = PharmacologicalEvaluation.objects.all()

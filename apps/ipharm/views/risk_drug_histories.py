from common.views import HistoryView
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models.risk_drug_histories import (
    RiskDrugHistory,
    RiskDrugHistoryComment,
    RiskDrugHistoryDiagnosis,
)
from ..serializers.risk_drug_histories import (
    RiskDrugHistoryCommentSerializer,
    RiskDrugHistoryDiagnosisSerializer,
    RiskDrugHistoryNestedSerializer,
    RiskDrugHistorySerializer,
)


class RiskDrugHistoryListView(generics.ListCreateAPIView):
    queryset = (
        RiskDrugHistory.objects.prefetch_related("comments")
        .prefetch_related(
            Prefetch(
                "diagnoses",
                queryset=RiskDrugHistoryDiagnosis.objects.select_related(
                    "diagnosis"
                ).prefetch_related("drugs"),
            )
        )
        .prefetch_related("tags")
        .all()
    )
    serializer_class = RiskDrugHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["care"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RiskDrugHistoryNestedSerializer
        return RiskDrugHistorySerializer


class RiskDrugHistoryDetailView(
    generics.RetrieveUpdateAPIView,
):
    queryset = RiskDrugHistory.objects.all()
    serializer_class = RiskDrugHistorySerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RiskDrugHistoryNestedSerializer
        return RiskDrugHistorySerializer


class RiskDrugHistoryHistoryView(HistoryView):
    queryset = RiskDrugHistory.objects.all()


class RiskDrugHistoryCommentListView(generics.ListCreateAPIView):
    queryset = RiskDrugHistoryComment.objects.all()
    serializer_class = RiskDrugHistoryCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["risk_drug_history"]


class RiskDrugHistoryCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RiskDrugHistoryComment.objects.all()
    serializer_class = RiskDrugHistoryCommentSerializer


class RiskDrugHistoryCommentHistoryView(HistoryView):
    queryset = RiskDrugHistoryComment.objects.all()


class RiskDrugHistoryDiagnosisListView(generics.ListCreateAPIView):
    queryset = RiskDrugHistoryDiagnosis.objects.all()
    serializer_class = RiskDrugHistoryDiagnosisSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["risk_drug_history"]


class RiskDrugHistoryDiagnosisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RiskDrugHistoryDiagnosis.objects.all()
    serializer_class = RiskDrugHistoryDiagnosisSerializer


class RiskDrugHistoryDiagnosisHistoryView(HistoryView):
    queryset = RiskDrugHistoryDiagnosis.objects.all()

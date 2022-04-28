from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models.risk_drug_histories import RiskDrugHistory, RiskDrugHistoryComment
from ..serializers.risk_drug_histories import (
    RiskDrugHistoryCommentSerializer,
    RiskDrugHistoryNestedSerializer,
    RiskDrugHistorySerializer,
)
from .common import HistoryView


class RiskDrugHistoryListView(generics.ListCreateAPIView):
    queryset = (
        RiskDrugHistory.objects.prefetch_related("comments")
        .prefetch_related("risk_drugs")
        .prefetch_related("risk_diagnoses")
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

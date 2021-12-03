from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models import RiskDrugHistory, RiskDrugHistoryComment
from ..serializers import (
    RiskDrugHistoryCommentSerializer,
    RiskDrugHistoryNestedSerializer,
    RiskDrugHistorySerializer,
)


class RiskDrugHistoryListView(generics.ListCreateAPIView):
    queryset = RiskDrugHistory.objects.all()
    serializer_class = RiskDrugHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["care"]


class RiskDrugHistoryDetailView(
    generics.RetrieveUpdateAPIView,
):
    queryset = RiskDrugHistory.objects.all()
    serializer_class = RiskDrugHistorySerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RiskDrugHistoryNestedSerializer
        return RiskDrugHistorySerializer


class RiskDrugHistoryCommentListView(generics.ListCreateAPIView):
    queryset = RiskDrugHistoryComment.objects.all()
    serializer_class = RiskDrugHistoryCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["risk_drug_history"]


class RiskDrugHistoryCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RiskDrugHistoryComment.objects.all()
    serializer_class = RiskDrugHistoryCommentSerializer

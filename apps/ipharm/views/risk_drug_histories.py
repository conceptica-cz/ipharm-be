from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models import RiskDrugHistory
from ..serializers import RiskDrugHistoryNestedSerializer, RiskDrugHistorySerializer


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

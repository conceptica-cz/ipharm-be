from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models import PatientInformation
from ..serializers import (
    PatientInformationNestedSerializer,
    PatientInformationSerializer,
)
from .common import HistoryView


class PatientInformationListView(generics.ListCreateAPIView):
    queryset = PatientInformation.objects.all()
    serializer_class = PatientInformationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["care"]


class PatientInformationDetailView(
    generics.RetrieveUpdateAPIView,
):
    queryset = PatientInformation.objects.all()
    serializer_class = PatientInformationSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PatientInformationNestedSerializer
        return PatientInformationSerializer


class PatientInformationHistoryView(HistoryView):
    queryset = PatientInformation.objects.all()

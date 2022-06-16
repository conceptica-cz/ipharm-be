from common.views import HistoryView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..filters.patient_informations import PatientInformationFilter
from ..models.patient_informations import PatientInformation
from ..serializers.patient_informations import (
    PatientInformationNestedSerializer,
    PatientInformationSerializer,
)


class PatientInformationListView(generics.ListCreateAPIView):
    queryset = PatientInformation.objects.all()
    serializer_class = PatientInformationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientInformationFilter


class PatientInformationDetailView(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = PatientInformation.objects.all()
    serializer_class = PatientInformationSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PatientInformationNestedSerializer
        return PatientInformationSerializer


class PatientInformationHistoryView(HistoryView):
    queryset = PatientInformation.objects.all()

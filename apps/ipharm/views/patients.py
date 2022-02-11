from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import SAFE_METHODS

from ..filters import PatientFilter
from ..models.patients import Patient
from ..serializers.patients import PatientNestedSerializer, PatientSerializer
from .common import HistoryView


class PatientListView(generics.ListCreateAPIView):
    queryset = (
        Patient.objects.select_related("current_care")
        .select_related("insurance_company")
        .select_related("current_care__clinic")
        .select_related("current_care__department")
        .select_related("current_care__main_diagnosis")
        .select_related("current_care__checkin")
        .select_related("current_care__pharmacologicalplan")
        .select_related("current_care__last_dekurz")
        .select_related("current_care__last_dekurz__doctor")
        .select_related("current_care__last_dekurz__department")
        .all()
    )
    serializer_class = PatientNestedSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PatientFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PatientNestedSerializer
        else:
            return PatientSerializer


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientNestedSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PatientNestedSerializer
        else:
            return PatientSerializer


class PatientHistoryView(HistoryView):
    queryset = Patient.objects.all()

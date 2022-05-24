from common.views import HistoryView
from django_filters.rest_framework import DjangoFilterBackend
from ipharm.filters.patients import PatientFilter
from ipharm.models.patients import Patient
from ipharm.serializers.patients import (
    PatientLiteNestedSerializer,
    PatientNestedSerializer,
    PatientSerializer,
)
from rest_framework import filters, generics
from rest_framework.permissions import SAFE_METHODS


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
        .filter(current_care__isnull=False)
    )
    serializer_class = PatientLiteNestedSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PatientFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PatientLiteNestedSerializer
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

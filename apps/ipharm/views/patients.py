from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import SAFE_METHODS

from ..models.patients import Patient
from ..serializers.patients import PatientNestedSerializer, PatientSerializer


class PatientListView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        "clinic",
        "patient_type",
        "patient_id",
        "birth_number",
        "last_name",
    ]
    search_fields = ["patient_id", "birth_number", "last_name"]


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientNestedSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PatientNestedSerializer
        else:
            return PatientSerializer

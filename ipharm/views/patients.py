from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from ipharm.models.patients import Clinic, Patient
from ipharm.serializers.patients import ClinicSerializer, PatientSerializer


class ClinicListView(generics.ListAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer


class ClinicDetailView(generics.RetrieveAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer


class PatientListView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["clinic"]
    search_fields = ["patient_id", "birth_number"]


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

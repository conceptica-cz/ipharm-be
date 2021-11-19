from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import SAFE_METHODS

from ..filters import PatientFilter
from ..models.patients import Patient
from ..serializers.patients import PatientNestedSerializer, PatientSerializer


class PatientListView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PatientFilter


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientNestedSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PatientNestedSerializer
        else:
            return PatientSerializer

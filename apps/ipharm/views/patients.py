from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from references.models.clinics import Clinic
from references.serializers.clinics import ClinicSerializer
from rest_framework import filters, generics

from ..models.patients import Patient
from ..serializers.patients import PatientSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="my_clinics_only",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="if true return only current user's 'my clinics'",
                default="false",
            )
        ]
    )
)
class ClinicListView(generics.ListAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["clinic_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get("my_clinics_only", "false").lower() == "true":
            queryset = queryset.filter(user=self.request.user)
        return queryset


class ClinicDetailView(generics.RetrieveAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer


class PatientListView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["clinic", "patient_id", "birth_number", "last_name"]
    search_fields = ["patient_id", "birth_number", "last_name"]


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

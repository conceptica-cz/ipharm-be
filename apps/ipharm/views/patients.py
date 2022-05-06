from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, generics
from rest_framework.permissions import SAFE_METHODS

from ..filters import PatientFilter
from ..models.patients import Patient
from ..serializers.patients import (
    PatientLiteNestedSerializer,
    PatientNestedSerializer,
    PatientSerializer,
)
from .common import HistoryView


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="age",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Age of the patient",
            ),
            OpenApiParameter(
                name="age_min",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Minimum age of the patient",
            ),
            OpenApiParameter(
                name="age_max",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Maximum age of the patient",
            ),
            OpenApiParameter(
                name="tag",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Tag ID of the patient",
            ),
        ]
    )
)
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

from common.views import HistoryView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS

from ..models.patients import Patient
from ..serializers.patients import (
    PatientLiteNestedSerializer,
    PatientNestedSerializer,
    PatientSerializer,
)


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
                name="birth_number",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Birth number of the patient",
            ),
            OpenApiParameter(
                name="birth_number__icontains",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Birth number of the patient contains",
            ),
            OpenApiParameter(
                name="care_type",
                enum=[
                    "hospitalization",
                    "ambulation",
                    "external",
                ],
                location=OpenApiParameter.QUERY,
                description="Type of care",
            ),
            OpenApiParameter(
                name="care_date_from",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="From date of the care (care started >= this date or care ended >= this date)",  # noqa
            ),
            OpenApiParameter(
                name="care_date_to",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="To date of the care (care ended <= this date)",  # noqa
            ),
            OpenApiParameter(
                name="clinic",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Clinic ID",
            ),
            OpenApiParameter(
                name="external_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="External (UNIS) ID of the patient",
            ),
            OpenApiParameter(
                name="first_name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="First name of the patient",
            ),
            OpenApiParameter(
                name="first_name__icontains",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="First name of the patient contains",
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Care is active (does not have `finished_at` date)",
            ),
            OpenApiParameter(
                name="is_locked",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Care is locked (finished earlier than 14 days)",
            ),
            OpenApiParameter(
                name="last_name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Last name of the patient",
            ),
            OpenApiParameter(
                name="last_name__icontains",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Last name of the patient contains",
            ),
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Name of the patient",
            ),
            OpenApiParameter(
                name="name__icontains",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Name of the patient contains",
            ),
            OpenApiParameter(
                name="tag",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Tag ID of the patient",
            ),
            OpenApiParameter(
                name="has_checkin",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="If true, returns only patients with CheckIn",
            ),
            OpenApiParameter(
                name="has_pharmacologicalplan",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="If true, returns only patients with PharmacologicalPlan",
            ),
        ]
    )
)
class PatientListView(generics.ListCreateAPIView):
    serializer_class = PatientLiteNestedSerializer

    def get_queryset(self):
        bool_params = [
            "has_checkin",
            "has_pharmacologicalplan",
            "is_active",
            "is_locked",
        ]
        params = self.request.query_params.dict()
        for param in bool_params:
            if param in params:
                params[param] = params[param] == "true"
        queryset = Patient.objects.filter_prefetched(**params)
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PatientLiteNestedSerializer
        else:
            return PatientSerializer


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.filter_prefetched()
    serializer_class = PatientNestedSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PatientNestedSerializer
        else:
            return PatientSerializer


class PatientHistoryView(HistoryView):
    queryset = Patient.objects.all()

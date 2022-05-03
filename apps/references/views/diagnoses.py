from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from references.filters import DiagnosisFilter
from references.models.diagnoses import Diagnosis
from references.serializers.diagnoses import DiagnosisSerializer
from rest_framework import filters, generics


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="clinical_pharmacology",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="if `true` returns only clinical pharmacology diagnoses",
                default="false",
            )
        ]
    )
)
class DiagnosisListView(generics.ListAPIView):
    """Diagnosis list"""

    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = DiagnosisFilter
    search_fields = ["code", "name"]


class DiagnosisDetailView(generics.RetrieveAPIView):
    """Diagnosis detail"""

    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

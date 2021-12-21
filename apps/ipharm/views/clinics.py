from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from references.models import Clinic, Department
from references.serializers import ClinicSerializer, DepartmentSerializer
from rest_framework import filters, generics


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="clinic_filter",
                enum=[
                    "all",
                    "hospitals",
                    "ambulances",
                    "my_hospitals",
                    "my_ambulances",
                ],
                location=OpenApiParameter.QUERY,
                description="if 'hospitals' returns only hospital clinics, 'abmulances' -> only ambulances,  'my_clinics'-> only user's clinics,  'my_ambulances'-> only user's ambulances",
                default="all",
            )
        ]
    )
)
class ClinicListView(generics.ListAPIView):
    serializer_class = ClinicSerializer

    def get_queryset(self):
        clinic_filter = self.request.query_params.get("clinic_filter", "all")
        if clinic_filter == "hospitals":
            queryset = Clinic.objects.get_hospitals()
        elif clinic_filter == "my_hospitals":
            queryset = Clinic.objects.get_my_hospitals(self.request.user)
        elif clinic_filter == "ambulances":
            queryset = Clinic.objects.get_ambulances()
        elif clinic_filter == "my_ambulances":
            queryset = Clinic.objects.get_my_ambulances(self.request.user)
        else:
            queryset = Clinic.objects.all()
        return queryset


class ClinicDetailView(generics.RetrieveAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer


class DepartmentListView(generics.ListAPIView):
    """Department list"""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["clinic"]
    search_fields = ["abbreviation", "description"]


class DepartmentDetailView(generics.RetrieveAPIView):
    """Department detail"""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

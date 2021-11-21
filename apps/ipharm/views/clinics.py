from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from references.models.clinics import Clinic
from references.serializers.clinics import ClinicSerializer
from rest_framework import generics


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
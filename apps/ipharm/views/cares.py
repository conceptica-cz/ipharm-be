from common.views import HistoryView
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.cares import Care
from ..models.checkins import CheckInDiagnosis
from ..serializers.cares import (
    CareNestedSerializer,
    CareProceduresSerializer,
    CareSerializer,
)
from ..services.cares import CareProcedures


class CareDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = (
        Care.objects.select_related("clinic")
        .select_related("department")
        .select_related("main_diagnosis")
        .select_related("last_dekurz")
        .select_related("last_dekurz__doctor")
        .select_related("last_dekurz__department")
        .select_related("checkin")
        .prefetch_related(
            Prefetch(
                "checkin__diagnoses",
                queryset=CheckInDiagnosis.objects.select_related("diagnosis"),
            ),
        )
        .prefetch_related("checkin__diagnoses__drugs")
        .select_related("pharmacologicalplan")
        .prefetch_related(("pharmacologicalplan__tags"))
        .prefetch_related("pharmacological_evaluations")
        .prefetch_related("pharmacological_evaluations__tags")
        .prefetch_related("requisitions")
    )
    serializer_class = CareNestedSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CareNestedSerializer
        else:
            return CareSerializer


class CareHistoryView(HistoryView):
    queryset = Care.objects.all()


@extend_schema_view(
    get=extend_schema(
        responses={
            status.HTTP_202_ACCEPTED: CareProceduresSerializer,
        },
    ),
)
class CareProceduresView(APIView):
    def get(self, request, *args, **kwargs):
        care = Care.objects.get(pk=kwargs["pk"])
        care_procedures = CareProcedures(care=care)
        care_procedures.count()
        return Response(CareProceduresSerializer(care_procedures).data)

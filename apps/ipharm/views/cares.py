from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.cares import Care
from ..serializers.cares import (
    CareNestedSerializer,
    CareProceduresSerializer,
    CareSerializer,
)
from ..services.cares import CareProcedures
from .common import HistoryView


class CareDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Care.objects.all()
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

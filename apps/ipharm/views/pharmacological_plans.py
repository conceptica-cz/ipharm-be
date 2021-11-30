from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models import PharmacologicalPlan
from ..serializers import (
    PharmacologicalPlanNestedSerializer,
    PharmacologicalPlanSerializer,
)


class PharmacologicalPlanListView(generics.ListCreateAPIView):
    queryset = PharmacologicalPlan.objects.all()
    serializer_class = PharmacologicalPlanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["care"]


class PharmacologicalPlanDetailView(
    generics.RetrieveUpdateAPIView,
):
    queryset = PharmacologicalPlan.objects.all()
    serializer_class = PharmacologicalPlanSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PharmacologicalPlanNestedSerializer
        return PharmacologicalPlanSerializer

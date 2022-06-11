from common.views import HistoryView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from updates.tasks import task_update_remote_requisition

from ..filters import RequisitionFilter
from ..models.requisitions import Requisition
from ..serializers.requisitions import (
    RequisitionNestedSerializer,
    RequisitionSerializer,
)


class RequisitionListView(generics.ListAPIView):
    queryset = (
        Requisition.objects.select_related("care")
        .select_related("applicant")
        .select_related("solver")
        .all()
    )

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RequisitionFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RequisitionNestedSerializer
        return RequisitionSerializer


class RequisitionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Requisition.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RequisitionNestedSerializer
        return RequisitionSerializer

    def perform_update(self, serializer):
        requisition = serializer.save(is_synced=False)
        task_update_remote_requisition.apply_async(
            kwargs={
                "requisition_id": requisition.pk,
                "fields_to_update": ["state", "solver"],
            },
            queue="high_priority",
        )


class RequisitionHistoryView(HistoryView):
    queryset = Requisition.objects.all()

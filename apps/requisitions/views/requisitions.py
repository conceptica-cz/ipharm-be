from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from ipharm.views.common import HistoryView
from rest_framework import filters, generics

from ..filters import RequisitionFilter
from ..models.requisitions import Requisition
from ..serializers.requisitions import (
    RequisitionNestedSerializer,
    RequisitionSerializer,
)


class RequisitionListView(generics.ListCreateAPIView):
    queryset = (
        Requisition.objects.select_related("patient")
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
        if self.request.user.is_app:
            serializer.save(is_synced=True, synced_at=timezone.now())
        else:
            serializer.save(is_synced=False)


class RequisitionHistoryView(HistoryView):
    queryset = Requisition.objects.all()

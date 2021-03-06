from common.views import HistoryView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)
from ..serializers.pharmacological_plans import (
    PharmacologicalPlanCommentSerializer,
    PharmacologicalPlanNestedSerializer,
    PharmacologicalPlanSerializer,
)


class PharmacologicalPlanListView(generics.ListCreateAPIView):
    queryset = PharmacologicalPlan.objects.prefetch_related("tags").prefetch_related(
        "comments"
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["care"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PharmacologicalPlanNestedSerializer
        return PharmacologicalPlanSerializer


class PharmacologicalPlanDetailView(
    generics.RetrieveUpdateAPIView,
):
    queryset = PharmacologicalPlan.objects.all()
    serializer_class = PharmacologicalPlanSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PharmacologicalPlanNestedSerializer
        return PharmacologicalPlanSerializer


class PharmacologicalPlanHistoryView(HistoryView):
    queryset = PharmacologicalPlan.objects.all()


class PharmacologicalPlanCommentListView(generics.ListCreateAPIView):
    queryset = PharmacologicalPlanComment.objects.select_related("author")
    serializer_class = PharmacologicalPlanCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["pharmacological_plan"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PharmacologicalPlanCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PharmacologicalPlanComment.objects.all()
    serializer_class = PharmacologicalPlanCommentSerializer


class PharmacologicalPlanCommentHistoryView(HistoryView):
    queryset = PharmacologicalPlanComment.objects.all()

from common.views import HistoryView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ..models.pharmacological_evaluations import (
    PharmacologicalEvaluation,
    PharmacologicalEvaluationComment,
)
from ..serializers.pharmacological_evaluations import (
    PharmacologicalEvaluationCommentSerializer,
    PharmacologicalEvaluationNestedSerializer,
    PharmacologicalEvaluationSerializer,
)


class PharmacologicalEvaluationListView(generics.ListCreateAPIView):
    queryset = PharmacologicalEvaluation.objects.prefetch_related("tags").all()
    serializer_class = PharmacologicalEvaluationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["care"]


class PharmacologicalEvaluationDetailView(
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = PharmacologicalEvaluation.objects.all()
    serializer_class = PharmacologicalEvaluationSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PharmacologicalEvaluationNestedSerializer
        return PharmacologicalEvaluationSerializer


class PharmacologicalEvaluationHistoryView(HistoryView):
    queryset = PharmacologicalEvaluation.objects.all()


class PharmacologicalEvaluationCommentListView(generics.ListCreateAPIView):
    queryset = PharmacologicalEvaluationComment.objects.select_related("author")
    serializer_class = PharmacologicalEvaluationCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["pharmacological_evaluation"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PharmacologicalEvaluationCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PharmacologicalEvaluationComment.objects.all()
    serializer_class = PharmacologicalEvaluationCommentSerializer


class PharmacologicalEvaluationCommentHistoryView(HistoryView):
    queryset = PharmacologicalEvaluationComment.objects.all()

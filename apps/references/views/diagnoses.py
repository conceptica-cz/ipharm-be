from references.models.diagnoses import Diagnosis
from references.serializers.diagnoses import DiagnosisSerializer
from rest_framework import filters, generics


class DiagnosisListView(generics.ListAPIView):
    """Diagnosis list"""

    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["code", "name"]


class DiagnosisDetailView(generics.RetrieveAPIView):
    """Diagnosis detail"""

    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer

from references.models import Drug
from references.serializers import DrugSerializer
from rest_framework import filters, generics


class DrugListView(generics.ListAPIView):
    """Drug list"""

    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["code_sukl", "name"]


class DrugDetailView(generics.RetrieveAPIView):
    """Drug detail"""

    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

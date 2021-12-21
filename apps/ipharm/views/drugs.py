from references.models import Drug
from references.serializers import DrugSerializer
from rest_framework import generics


class DrugListView(generics.ListAPIView):
    """Drug list"""

    queryset = Drug.objects.all()
    serializer_class = DrugSerializer


class DrugDetailView(generics.RetrieveAPIView):
    """Drug detail"""

    queryset = Drug.objects.all()
    serializer_class = DrugSerializer

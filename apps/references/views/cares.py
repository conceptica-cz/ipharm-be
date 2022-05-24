from common.views import HistoryView
from rest_framework import generics
from rest_framework.permissions import SAFE_METHODS

from ..models.cares import Care
from ..serializers.cares import CareNestedSerializer, CareSerializer


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

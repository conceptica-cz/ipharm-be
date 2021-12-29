from rest_framework import generics

from ..models import CheckIn
from ..serializers import CheckInNestedSerializer, CheckInSerializer
from .common import HistoryView


class CheckInListView(generics.ListCreateAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer


class CheckInDetailView(generics.RetrieveUpdateAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CheckInNestedSerializer
        return CheckInSerializer


class CheckInHistoryView(HistoryView):
    queryset = CheckIn.objects.all()

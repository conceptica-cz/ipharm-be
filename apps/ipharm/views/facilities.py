from references.models import MedicalFacility
from references.serializers import MedicalFacilitySerializer
from rest_framework import filters, generics


class MedicalFacilityListView(generics.ListAPIView):
    """MedicalFacility list"""

    queryset = MedicalFacility.objects.all()
    serializer_class = MedicalFacilitySerializer


class MedicalFacilityDetailView(generics.RetrieveAPIView):
    """MedicalFacility detail"""

    queryset = MedicalFacility.objects.all()
    serializer_class = MedicalFacilitySerializer

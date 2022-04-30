from references.models.insurances import InsuranceCompany
from references.serializers.insurances import InsuranceCompanySerializer
from rest_framework import filters, generics


class InsuranceCompanyListView(generics.ListAPIView):
    """InsuranceCompany list"""

    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["code", "name", "shortcut"]


class InsuranceCompanyDetailView(generics.RetrieveAPIView):
    """InsuranceCompany detail"""

    queryset = InsuranceCompany.objects.all()
    serializer_class = InsuranceCompanySerializer

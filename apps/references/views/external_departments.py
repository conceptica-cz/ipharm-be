from references.models import ExternalDepartment
from references.serializers import ExternalDepartmentSerializer
from rest_framework import filters, generics


class ExternalDepartmentListView(generics.ListAPIView):
    """ExternalDepartment list"""

    queryset = ExternalDepartment.objects.all()
    serializer_class = ExternalDepartmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["icp", "organization", "department"]


class ExternalDepartmentDetailView(generics.RetrieveAPIView):
    """ExternalDepartment detail"""

    queryset = ExternalDepartment.objects.all()
    serializer_class = ExternalDepartmentSerializer

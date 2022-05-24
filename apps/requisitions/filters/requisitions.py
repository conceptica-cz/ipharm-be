import django_filters
from requisitions.models.requisitions import Requisition


class RequisitionFilter(django_filters.FilterSet):
    class Meta:
        model = Requisition
        fields = {
            "id": [
                "exact",
            ],
        }

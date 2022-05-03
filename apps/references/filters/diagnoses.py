import django_filters
from django.db.models import Q
from references.models.diagnoses import Diagnosis


class DiagnosisFilter(django_filters.FilterSet):
    @staticmethod
    def _get_codes():
        codes = [
            "E10",
            "E11",
            "E12",
            "E13",
            "E14",
            "G40",
            "G41",
            "I48",
            "G20",
            "G21",
        ]
        codes.extend([f"C0{i}" for i in range(0, 10)])
        codes.extend([f"C{i}" for i in range(10, 98)])
        return codes

    def filter_clinical_pharmacology(self, queryset, name, value):
        if value:
            codes = self._get_codes()
            filters = Q(code__startswith=codes[0])
            for code in codes[1:]:
                filters |= Q(code__startswith=code)
            return queryset.filter(filters)
        return queryset

    clinical_pharmacology = django_filters.BooleanFilter(
        method="filter_clinical_pharmacology"
    )

    class Meta:
        model = Diagnosis
        fields = ["code"]

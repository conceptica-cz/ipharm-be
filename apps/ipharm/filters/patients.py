import django_filters
from ipharm.models import Patient


class PatientFilter(django_filters.FilterSet):
    clinic = django_filters.NumberFilter(field_name="current_care__clinic__pk")

    care_type = django_filters.CharFilter(field_name="current_care__care_type")

    class Meta:
        model = Patient
        fields = {
            "birth_number": ["exact", "icontains"],
            "name": ["exact", "icontains"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
        }

import django_filters
from ipharm.models import Patient


class PatientFilter(django_filters.FilterSet):
    hospital = django_filters.NumberFilter(
        field_name="current_hospital_care__clinic__pk"
    )
    ambulance = django_filters.NumberFilter(
        field_name="current_ambulance_care__clinic__pk"
    )

    class Meta:
        model = Patient
        fields = {
            "birth_number": ["exact", "icontains"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
        }

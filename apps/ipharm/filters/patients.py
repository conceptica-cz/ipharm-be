import django_filters
from ipharm.models import Patient


class PatientFilter(django_filters.FilterSet):
    clinic = django_filters.NumberFilter(field_name="current_care__clinic__pk")

    care_type = django_filters.CharFilter(field_name="current_care__care_type")

    has_checkin = django_filters.BooleanFilter(
        field_name="current_care__checkin", lookup_expr="isnull", exclude=True
    )

    has_pharmacologicalplan = django_filters.BooleanFilter(
        field_name="current_care__pharmacologicalplan",
        lookup_expr="isnull",
        exclude=True,
    )

    is_active = django_filters.BooleanFilter(field_name="current_care__is_active")

    risk_level = django_filters.CharFilter(
        field_name="current_care__checkin__risk_level", lookup_expr="exact"
    )

    has_notification_datetime = django_filters.BooleanFilter(
        field_name="current_care__pharmacologicalplan__notification_datetime",
        lookup_expr="isnull",
        exclude=True,
    )

    class Meta:
        model = Patient
        fields = {
            "birth_number": ["exact", "icontains"],
            "name": ["exact", "icontains"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
        }

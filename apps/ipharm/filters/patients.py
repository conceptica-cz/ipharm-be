from datetime import date

import django_filters
from django.db.models import Q
from django.utils import timezone
from ipharm.models.patients import Patient


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

    def filter_age(self, queryset, name, value):
        now = timezone.now()
        birth_date_min = date(now.year - value, now.month, now.day)
        birth_date_max = date(now.year - value + 1, now.month, now.day)
        return queryset.filter(birth_date__range=(birth_date_min, birth_date_max))

    def filter_age_min(self, queryset, name, value):
        now = timezone.now()
        birth_date_max = date(now.year - value + 1, now.month, now.day)
        return queryset.filter(birth_date__lte=birth_date_max)

    def filter_age_max(self, queryset, name, value):
        now = timezone.now()
        birth_date_min = date(now.year - value, now.month, now.day)
        return queryset.filter(birth_date__gte=birth_date_min)

    age = django_filters.NumberFilter(method="filter_age")
    age_min = django_filters.NumberFilter(method="filter_age_min")
    age_max = django_filters.NumberFilter(method="filter_age_max")

    def filter_tag(self, queryset, name, value):
        q = (
            Q(current_care__pharmacologicalplan__tags__id=value)
            | Q(current_care__riskdrughistory__tags__id=value)
            | Q(current_care__pharmacological_evaluations__tags__id=value)
        )
        queryset = queryset.filter(q).distinct()
        return queryset

    tag = django_filters.CharFilter(method="filter_tag")

    class Meta:
        model = Patient
        fields = {
            "birth_number": ["exact", "icontains"],
            "external_id": ["exact"],
            "name": ["exact", "icontains"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
        }

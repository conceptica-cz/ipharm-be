from django.conf import settings
from django.db.models import Prefetch, Q, QuerySet
from django.utils import timezone
from django.utils.datetime_safe import date
from ipharm.models.cares import Care


def filter_age(value):
    value = int(value)
    now = timezone.now()
    birth_date_min = date(now.year - value, now.month, now.day)
    birth_date_max = date(now.year - value + 1, now.month, now.day)
    return Q(birth_date__range=(birth_date_min, birth_date_max))


def fitler_age_min(value):
    value = int(value)
    now = timezone.now()
    birth_date_max = date(now.year - value + 1, now.month, now.day)
    return Q(birth_date__lte=birth_date_max)


def filter_age_max(value):
    value = int(value)
    now = timezone.now()
    birth_date_min = date(now.year - value, now.month, now.day)
    return Q(birth_date__gte=birth_date_min)


def tag_patient_filter(value):
    return (
        Q(cares__pharmacologicalplan__tags__id=value)
        | Q(cares__riskdrughistory__tags__id=value)
        | Q(cares__pharmacological_evaluations__tags__id=value)
    )


def tag_care_filter(value):
    return (
        Q(pharmacologicalplan__tags__id=value)
        | Q(riskdrughistory__tags__id=value)
        | Q(pharmacological_evaluations__tags__id=value)
    )


def is_locked_patient_filter(value):
    threshold = timezone.now() - timezone.timedelta(days=settings.CARE_LOCK_TIME_GAP)
    if value:
        return Q(cares__finished_at__isnull=False) & Q(
            cares__finished_at__lte=threshold
        )
    else:
        return Q(cares__finished_at__isnull=True) | Q(cares__finished_at__gt=threshold)


def is_locked_care_filter(value):
    threshold = timezone.now() - timezone.timedelta(days=settings.CARE_LOCK_TIME_GAP)
    if value:
        return Q(finished_at__isnull=False) & Q(finished_at__lte=threshold)
    else:
        return Q(finished_at__isnull=True) | Q(finished_at__gt=threshold)


def care_date_from_care_filter(value):
    return Q(started_at__gte=value) | (
        Q(finished_at__isnull=True) | Q(finished_at__gte=value)
    )


def care_date_from_patient_filter(value):
    return Q(cares__started_at__gte=value) | (
        Q(cares__finished_at__isnull=True) | Q(cares__finished_at__gte=value)
    )


def care_date_to_care_filter(value):
    return Q(finished_at__lte=value)


def care_date_to_patient_filter(value):
    return Q(cares__finished_at__lte=value)


class PatientQuerySet(QuerySet):
    def filter_prefetched(self, **kwargs):
        """Filter patients and prefetched cares"""

        lookups = {
            "birth_number": {
                "patient_lookup": "birth_number",
            },
            "birth_number__icontains": {
                "patient_lookup": "birth_number__icontains",
            },
            "external_id": {
                "patient_lookup": "external_id",
            },
            "name": {
                "patient_lookup": "name",
            },
            "name__icontains": {
                "patient_lookup": "name__icontains",
            },
            "first_name": {
                "patient_lookup": "first_name",
            },
            "first_name__icontains": {
                "patient_lookup": "first_name__icontains",
            },
            "last_name": {
                "patient_lookup": "last_name",
            },
            "last_name__icontains": {
                "patient_lookup": "last_name__icontains",
            },
            "clinic": {
                "patient_lookup": "cares__clinic",
                "care_lookup": "clinic",
            },
            "is_active": {
                "patient_lookup": "cares__is_active",
                "care_lookup": "is_active",
            },
            "care_type": {
                "patient_lookup": "cares__care_type",
                "care_lookup": "care_type",
            },
            "risk_level": {
                "patient_lookup": "cares__checkin__risk_level",
                "care_lookup": "checkin__risk_level",
            },
            "is_locked": {
                "patient_filter": is_locked_patient_filter,
                "care_filter": is_locked_care_filter,
            },
            "care_date_from": {
                "patient_filter": care_date_from_patient_filter,
                "care_filter": care_date_from_care_filter,
            },
            "care_date_to": {
                "patient_filter": care_date_to_patient_filter,
                "care_filter": care_date_to_care_filter,
            },
            "tag": {
                "patient_filter": tag_patient_filter,
                "care_filter": tag_care_filter,
            },
            "age": {"patient_filter": filter_age},
            "age_min": {"patient_filter": fitler_age_min},
            "age_max": {"patient_filter": filter_age_max},
            "has_checkin": {
                "patient_filter": lambda v: Q(cares__checkin__isnull=not v),
                "care_filter": lambda v: Q(checkin__isnull=not v),
            },
            "has_pharmacologicalplan": {
                "patient_filter": lambda v: Q(cares__pharmacologicalplan__isnull=not v),
                "care_filter": lambda v: Q(pharmacologicalplan__isnull=not v),
            },
            "has_notification_datetime": {
                "patient_filter": lambda v: Q(
                    cares__pharmacologicalplan__notification_datetime__isnull=not v
                ),
                "care_filter": lambda v: Q(
                    pharmacologicalplan__notification_datetime__isnull=not v
                ),
            },
        }

        patient_filter = self._patient_filter(lookups, **kwargs)
        care_filter = self._care_filter(lookups, **kwargs)

        care_qs = (
            Care.objects.filter(care_filter)
            .distinct()
            .select_related("clinic")
            .select_related("department")
            .select_related("main_diagnosis")
            .select_related("last_dekurz")
            .select_related("last_dekurz__doctor")
            .select_related("last_dekurz__department")
            .select_related("checkin")
            .select_related("pharmacologicalplan")
            .prefetch_related("requisitions")
        )
        queryset = (
            self.select_related("current_care")
            .select_related("insurance_company")
            .select_related("current_care__clinic")
            .select_related("current_care__department")
            .select_related("current_care__main_diagnosis")
            .select_related("current_care__last_dekurz")
            .select_related("current_care__checkin")
            .select_related("current_care__pharmacologicalplan")
            .select_related("current_care__last_dekurz__doctor")
            .select_related("current_care__last_dekurz__department")
            .filter(patient_filter)
            .distinct()
            .prefetch_related("current_care__requisitions")
            .prefetch_related(Prefetch("cares", queryset=care_qs))
        )

        return queryset

    @staticmethod
    def _patient_filter(lookups, **kwargs):
        patient_filter = Q()
        for key, value in kwargs.items():
            if key in lookups:
                if "patient_lookup" in lookups[key]:
                    lookup = lookups[key]["patient_lookup"]
                    patient_filter &= Q(**{lookup: value})
                elif "patient_filter" in lookups[key]:
                    patient_filter &= lookups[key]["patient_filter"](value)
        return patient_filter

    @staticmethod
    def _care_filter(lookups, **kwargs):
        care_filter = Q()
        for key, value in kwargs.items():
            if key in lookups:
                if "care_lookup" in lookups[key]:
                    lookup = lookups[key]["care_lookup"]
                    care_filter &= Q(**{lookup: value})
                elif "care_filter" in lookups[key]:
                    care_filter &= lookups[key]["care_filter"](value)
        return care_filter

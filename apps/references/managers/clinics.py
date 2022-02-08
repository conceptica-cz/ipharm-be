from django.db.models import Count, Q
from updates.managers import BaseTemporaryCreatableManager


class ClinicManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "description": "TMP",
        "abbreviation": "TMP",
    }

    def get_with_counters(self):
        """Return clinics with  patient counters"""
        queryset = self.get_queryset()
        queryset = queryset.annotate(
            patient_count=Count("care"),
            patient_without_checkin_count=Count(
                "care", filter=Q(care__checkin__isnull=True)
            ),
        )
        return queryset

    def get_hospitals(self):
        """Return only hospital clinics"""
        return self.get_with_counters().filter(is_hospital=True)

    def get_ambulances(self):
        """Return only ambulance clinics"""
        return self.get_with_counters().filter(is_ambulance=True)

    def get_my_hospitals(self, user):
        """Return clinics belonging to user"""
        return self.get_with_counters().filter(hospital_users=user)

    def get_my_ambulances(self, user):
        """Return ambulances belonging to user"""
        return self.get_with_counters().filter(ambulance_users=user)

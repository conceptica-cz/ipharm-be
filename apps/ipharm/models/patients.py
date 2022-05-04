import logging

from django.conf import settings
from django.db import models
from django.utils import timezone
from ipharm.managers.patients import PatientManager
from ipharm.services import cares
from updates.models import BaseUpdatableModel

logger = logging.getLogger(__name__)


class Patient(BaseUpdatableModel):
    external_id = models.CharField(
        "UNIS ID", max_length=50, null=True, blank=True, unique=True
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(db_index=True)
    birth_number = models.CharField(unique=True, max_length=10)
    insurance_company = models.ForeignKey(
        "references.InsuranceCompany", on_delete=models.SET_NULL, null=True, blank=True
    )
    insurance_number = models.CharField(max_length=100, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    current_care = models.OneToOneField(
        "Care",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patient_current_care",
    )
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    note = models.TextField(blank=True)

    objects = PatientManager()

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def set_current_care(self, care):
        if self.current_care:
            if self.current_care.started_at <= care.started_at:
                old_care = self.current_care
                old_care.finish()
                self.current_care = care
                self.save()

                if care.started_at - old_care.finished_at < timezone.timedelta(
                    hours=settings.MIGRATE_RELATED_TIME_GAP
                ):
                    cares.migrate_related(old_care, care)
            else:
                care.finish()
        else:
            self.current_care = care
            self.save()

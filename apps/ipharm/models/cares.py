from django.conf import settings
from django.db import models
from django.utils import timezone
from updates.models import BaseUpdatableModel


class CareIsLocked(Exception):
    pass


class Care(BaseUpdatableModel):
    HOSPITALIZATION = "hospitalization"
    AMBULATION = "ambulation"
    EXTERNAL = "external"

    CARE_TYPE_CHOICES = (
        (HOSPITALIZATION, "Hospitalization"),
        (AMBULATION, "Ambulation"),
        (EXTERNAL, "External"),
    )
    patient = models.ForeignKey(
        "Patient", on_delete=models.CASCADE, related_name="cares"
    )
    care_type = models.CharField(
        max_length=20, choices=CARE_TYPE_CHOICES, default=AMBULATION
    )
    is_active = models.BooleanField(default=True)
    main_diagnosis = models.ForeignKey(
        "references.Diagnosis",
        on_delete=models.SET_NULL,
        related_name="main_diagnosis",
        blank=True,
        null=True,
    )
    external_id = models.CharField("UNIS ID", max_length=50, null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    clinic = models.ForeignKey(
        "references.Clinic", on_delete=models.SET_NULL, null=True, blank=True
    )
    department = models.ForeignKey(
        "references.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients",
    )
    last_dekurz = models.OneToOneField(
        "Dekurz",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="last_dekurz_care",
    )
    external_department = models.ForeignKey(
        "references.ExternalDepartment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    doctor = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        unique_together = ("external_id", "clinic")

    def set_last_dekurz(self, dekurz):
        self.last_dekurz = dekurz
        self.save()

    def finish(self):
        if self.finished_at is None:
            self.finished_at = timezone.now()
            self.save()
        if self.is_active is True:
            self.is_active = False
            self.save()

    @property
    def actual_department(self):
        if self.department:
            return self.department
        return self.external_department

    @property
    def is_locked(self):
        if self.finished_at is None:
            return False
        if timezone.now() - self.finished_at > timezone.timedelta(
            days=settings.CARE_LOCK_TIME_GAP
        ):
            return True
        return False


class Dekurz(BaseUpdatableModel):
    care = models.ForeignKey("Care", on_delete=models.CASCADE)
    made_at = models.DateTimeField(null=True, blank=True)
    doctor = models.ForeignKey(
        "references.Person", on_delete=models.SET_NULL, null=True, blank=True
    )
    department = models.ForeignKey(
        "references.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients_dekurz",
    )

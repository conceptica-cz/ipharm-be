from django.db import models
from updates.models import BaseUpdatableModel


class Care(BaseUpdatableModel):
    HOSPITALIZATION = "hospitalization"
    AMBULATION = "ambulation"

    CARE_TYPE_CHOICES = (
        (HOSPITALIZATION, "Hospitalization"),
        (AMBULATION, "Ambulation"),
    )
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
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
    diagnoses = models.ManyToManyField("references.Diagnosis")
    external_id = models.CharField(
        "UNIS ID", max_length=50, null=True, blank=True, unique=True
    )
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    clinic = models.ForeignKey(
        "references.Clinic", on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(
        "references.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients",
    )
    dekurzes = models.ManyToManyField("Dekurz", related_name="dekurz_cares")
    last_dekurz = models.ForeignKey(
        "Dekurz",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="last_dekurz_care",
    )

    def add_dekurz(self, dekurz):
        self.dekurzes.add(dekurz)
        self.last_dekurz = dekurz
        self.save()


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

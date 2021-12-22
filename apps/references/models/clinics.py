from django.db import models
from updates.models import BaseUpdatableModel

from ..managers.clinics import ClinicManager
from ..managers.departments import DepartmentManager


class Clinic(BaseUpdatableModel):
    external_id = models.IntegerField(unique=True, help_text="UNIS Kód")
    abbreviation = models.CharField(max_length=10, help_text="Zkratka")
    description = models.CharField(max_length=255, db_index=True, help_text="Název")
    is_hospital = models.BooleanField(default=True, help_text="Ambulance")
    is_ambulance = models.BooleanField(default=False, help_text="Lůžkové oddělení")
    image = models.ImageField(
        upload_to="clinics", blank=True, null=True, help_text="Obrázek"
    )

    objects = ClinicManager()

    class Meta:
        ordering = ["description"]
        indexes = [
            models.Index(fields=["description"]),
        ]

    def __str__(self):
        return self.description


class Department(BaseUpdatableModel):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, help_text="Klinika")
    clinic_external_id = models.IntegerField(help_text="UNIS Kód kliniky")
    external_id = models.IntegerField(unique=True, help_text="UNIS Kód")
    abbreviation = models.CharField(max_length=10, help_text="Zkratka")
    description = models.CharField(max_length=255, help_text="Název")
    specialty = models.CharField(max_length=255, help_text="Odbornost")
    icp = models.CharField(max_length=255, help_text="IČP")

    class Meta:
        ordering = ["description"]
        indexes = [
            models.Index(fields=["description"]),
        ]

    objects = DepartmentManager()

    def __str__(self):
        return self.description

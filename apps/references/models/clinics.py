from django.db import models
from updates.models import BaseUpdatableModel

from ..managers.clinics import ClinicManager
from ..managers.departments import DepartmentManager


class Clinic(BaseUpdatableModel):
    external_id = models.IntegerField(
        unique=True, blank=True, null=True, help_text="UNIS Kód"
    )
    reference_id = models.IntegerField(
        unique=True, blank=True, null=True, help_text="iČíselník Kód"
    )
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
    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, blank=True, null=True, help_text="Klinika"
    )
    external_id = models.IntegerField(
        unique=True, blank=True, null=True, help_text="UNIS Kód"
    )
    abbreviation = models.CharField(max_length=10, help_text="Zkratka")
    description = models.CharField(max_length=255, help_text="Název")
    specialization_code = models.CharField(
        max_length=3, blank=True, help_text="Odbornost (kód)"
    )
    icp = models.CharField(max_length=8, help_text="IČP")
    ns = models.CharField(max_length=6, blank=True, help_text="Nákladove středisko")
    workplace_code = models.CharField(
        max_length=10, blank=True, help_text="Zkrácený kód pracoviště dle ÚZIS"
    )
    for_insurance = models.BooleanField(
        blank=True,
        null=True,
        unique=True,
        help_text="Používat pro vykazování pojištění",
    )

    class Meta:
        ordering = ["description"]
        indexes = [
            models.Index(fields=["description"]),
        ]

    objects = DepartmentManager()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.for_insurance == False:  # prevent unique constraint violation
            self.for_insurance = None
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.description

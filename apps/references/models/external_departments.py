from django.db import models
from updates.models import BaseUpdatableModel


class ExternalDepartment(BaseUpdatableModel):
    icp = models.CharField(max_length=8, unique=True, help_text="IČP")
    organization = models.CharField(
        max_length=255, help_text="Název organizace (zařízení)"
    )
    department = models.CharField(
        max_length=255, blank=True, help_text="Název oddělení"
    )
    specialization_code = models.CharField(
        max_length=3, blank=True, help_text="Odbornost (kód)"
    )

    class Meta:
        ordering = ["organization"]

    def __str__(self):
        return self.organization

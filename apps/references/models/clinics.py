from django.db import models
from updates.models import BaseUpdatableModel


class Clinic(BaseUpdatableModel):
    CLINIC = "clinic"
    AMBULANCE = "ambulance"
    TYPE_CHOICES = (
        (CLINIC, "Clinic"),
        (AMBULANCE, "Ambulance"),
    )
    clinic_id = models.IntegerField()
    abbreviation = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    clinic_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=CLINIC)

    class Meta:
        unique_together = ["clinic_type", "clinic_id"]

    def __str__(self):
        return self.description

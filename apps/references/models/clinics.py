from django.db import models
from updates.models import BaseUpdatableModel

from ..managers.clinics import ClinicManager


class Clinic(BaseUpdatableModel):
    external_id = models.IntegerField(unique=True)
    abbreviation = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    is_hospital = models.BooleanField(default=True)
    is_ambulance = models.BooleanField(default=False)

    objects = ClinicManager()

    def __str__(self):
        return self.description


class Department(BaseUpdatableModel):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    clinic_external_id = models.IntegerField()
    external_id = models.IntegerField(unique=True)
    abbreviation = models.CharField(max_length=10)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

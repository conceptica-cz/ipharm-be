from django.db import models
from references.managers.diagnosis import DiagnosisManager
from updates.models import BaseUpdatableModel


class Diagnosis(BaseUpdatableModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    objects = DiagnosisManager()

    class Meta:
        verbose_name = "Diagnosis"
        verbose_name_plural = "Diagnoses"

    def __str__(self):
        return self.name

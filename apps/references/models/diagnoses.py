from django.db import models
from updates.models import BaseUpdatableModel


class Diagnosis(BaseUpdatableModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Diagnosis"
        verbose_name_plural = "Diagnoses"

    def __str__(self):
        return self.name

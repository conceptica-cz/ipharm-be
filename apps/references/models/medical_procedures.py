from django.db import models
from updates.models import BaseUpdatableModel


class MedicalProcedure(BaseUpdatableModel):
    """
    Model for medical procedures.
    """

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, blank=True)
    scores = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

from django.db import models
from updates.models import BaseUpdatableModel


class AdverseEffect(BaseUpdatableModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name

from django.db import models
from updates.models import BaseUpdatableModel


class InsuranceCompany(BaseUpdatableModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]
        verbose_name = "Insurance Company"
        verbose_name_plural = "Insurance Companies"

    def __str__(self):
        return self.name

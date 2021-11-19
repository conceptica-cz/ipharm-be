from django.db import models
from updates.models import BaseUpdatableModel


class Drug(BaseUpdatableModel):
    code_sukl = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

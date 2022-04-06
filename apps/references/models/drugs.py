from django.db import models
from updates.models import BaseUpdatableModel


class Drug(BaseUpdatableModel):
    code_sukl = models.CharField(max_length=50, unique=True, help_text="Kód SÚKL")
    name = models.CharField(max_length=255, help_text="Název léku")
    name_supplement = models.CharField(
        max_length=255, blank=True, help_text="Doplněk názvu"
    )
    atc_group = models.CharField(max_length=255, blank=True, help_text="ATC skupina")

    def __str__(self):
        return self.name

    def serialize(self):
        from references.serializers import DrugSerializer

        return DrugSerializer(self)

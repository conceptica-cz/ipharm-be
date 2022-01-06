from django.db import models
from references.managers.identifications import IdentificationManager
from updates.models import BaseUpdatableModel


class Identification(BaseUpdatableModel):
    name = models.CharField(
        max_length=100, unique=True, help_text="Název zdravotnického zařízení"
    )
    shortcut = models.CharField(
        max_length=20, null=True, blank=True, unique=True, help_text="Zkratka"
    )
    identifier = models.IntegerField(help_text="Identifikační číslo zařízení")
    address = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ulice",
    )
    zip = models.CharField(max_length=20, help_text="PSČ")
    city = models.CharField(max_length=50, help_text="Město")
    ico = models.CharField(max_length=20, blank=True, help_text="IČO")
    dic = models.CharField(max_length=20, blank=True, help_text="DIČ")
    for_insurance = models.BooleanField(
        blank=True,
        null=True,
        unique=True,
        help_text="Používat pro vykazování pojištění",
    )

    objects = IdentificationManager()

    def __str__(self):
        return self.name

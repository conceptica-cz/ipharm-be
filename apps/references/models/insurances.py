from django.db import models
from references.managers.insurances import InsuranceCompanyManager
from updates.models import BaseUpdatableModel


class InsuranceCompany(BaseUpdatableModel):
    code = models.CharField(max_length=20, unique=True, help_text="Kód")
    name = models.CharField(max_length=255, unique=True, help_text="Název")
    shortcut = models.CharField(
        max_length=20, null=True, blank=True, unique=True, help_text="Zkratka"
    )
    address = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ulice",
    )
    zip = models.CharField(max_length=20, help_text="PSČ")
    city = models.CharField(max_length=50, help_text="Město")
    ico = models.CharField(max_length=20, blank=True, help_text="IČO")
    dic = models.CharField(max_length=20, blank=True, help_text="DIČ")
    databox = models.CharField(max_length=10, blank=True, help_text="Databox")

    objects = InsuranceCompanyManager()

    class Meta:
        ordering = ["name"]
        verbose_name = "Insurance Company"
        verbose_name_plural = "Insurance Companies"

    def __str__(self):
        return self.name

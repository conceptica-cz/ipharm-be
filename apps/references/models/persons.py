from django.db import models
from references.managers.persons import PersonManager
from updates.models import BaseUpdatableModel


class Person(BaseUpdatableModel):
    person_number = models.CharField(
        max_length=100, unique=True, help_text="Osobní číslo"
    )
    name = models.CharField(max_length=255, help_text="Jméno")
    f_title = models.CharField(max_length=100, default="", help_text="Titul před")
    l_title = models.CharField(max_length=100, default="", help_text="Titul za")

    objects = PersonManager()

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

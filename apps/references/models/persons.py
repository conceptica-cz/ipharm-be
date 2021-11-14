from django.db import models
from references.managers.persons import PersonManager
from updates.models import BaseUpdatableModel


class Person(BaseUpdatableModel):
    person_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    f_title = models.CharField(max_length=100, default="")
    l_title = models.CharField(max_length=100, default="")

    objects = PersonManager()

    def __str__(self):
        return self.name

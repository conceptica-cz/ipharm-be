from common.models import BaseHistoricalModel
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager


class User(AbstractUser, BaseHistoricalModel):
    is_system = models.BooleanField(default=False)
    hospitals = models.ManyToManyField(
        "references.Clinic",
        related_name="hospital_users",
        verbose_name="My hospitals",
        blank=True,
    )
    ambulances = models.ManyToManyField(
        "references.Clinic",
        related_name="ambulance_users",
        verbose_name="My ambulances",
        blank=True,
    )

    objects = UserManager()

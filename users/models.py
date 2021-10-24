from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel
from ipharm.models import Clinic


class User(AbstractUser, BaseModel):
    is_system = models.BooleanField(default=False)
    clinics = models.ManyToManyField(Clinic, verbose_name="My clinics")

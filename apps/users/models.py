from common.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, BaseModel):
    is_system = models.BooleanField(default=False)
    clinics = models.ManyToManyField("references.Clinic", verbose_name="My clinics")

from common.models import BaseHistoricalModel
from django.contrib.auth.models import AbstractUser, Group
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

    def add_to_ipharm_group(self):
        """Add the 'ipharm' group to user"""
        if not self.in_ipharm_group():
            group, _ = Group.objects.get_or_create(name="ipharm")
            self.groups.add(group)

    def in_ipharm_group(self):
        """Return True if user is in the 'ipharm' group"""
        return self.groups.filter(name="ipharm").exists()

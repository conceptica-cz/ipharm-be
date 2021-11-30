from django.db import models
from ipharm.models import Care
from updates.models import BaseUpdatableModel


class PatientInformation(BaseUpdatableModel):
    care = models.ForeignKey(Care, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Název záznamu")
    text = models.TextField(blank=True, null=True, help_text="Popis")

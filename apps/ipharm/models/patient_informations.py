from django.db import models
from django.utils import timezone
from updates.models import BaseUpdatableModel


class PatientInformation(BaseUpdatableModel):
    care = models.ForeignKey(
        "ipharm.Care", related_name="patient_informations", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, help_text="Název záznamu")
    text = models.TextField(blank=True, null=True, help_text="Popis")
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    file = models.FileField(
        blank=True, null=True, upload_to="patient_information/", help_text="Soubor"
    )

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        return super().delete(using, keep_parents)

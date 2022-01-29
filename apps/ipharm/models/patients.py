from django.db import models
from django.utils import timezone
from ipharm.managers.patients import PatientManager
from updates.models import BaseUpdatableModel


class Patient(BaseUpdatableModel):
    external_id = models.CharField(
        "UNIS ID", max_length=50, null=True, blank=True, unique=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_number = models.CharField(unique=True, max_length=10)
    insurance_company = models.ForeignKey(
        "references.InsuranceCompany", on_delete=models.SET_NULL, null=True, blank=True
    )
    insurance_number = models.CharField(max_length=100, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    current_hospital_care = models.OneToOneField(
        "Care",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hospital_pacient",
    )
    current_ambulance_care = models.OneToOneField(
        "Care",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="amubulance_patient",
    )
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = PatientManager()

    class Meta:
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def set_current_care(self, care):
        if care.care_type == "hospitalization":
            self.current_hospital_care = care
        else:
            self.current_ambulance_care = care
        self.save()

from typing import List

from django.db import models
from updates.models import BaseUpdatableModel


class Patient(BaseUpdatableModel):
    HOSPITAL = "hospital"
    AMBULANCE = "ambulance"

    PATIENT_TYPE_CHOICES = (
        (HOSPITAL, "Hospital"),
        (AMBULANCE, "Ambulance"),
    )

    clinic = models.ForeignKey("references.Clinic", on_delete=models.CASCADE)
    patient_type = models.CharField(
        max_length=20, choices=PATIENT_TYPE_CHOICES, default=HOSPITAL
    )
    record_id = models.BigIntegerField(unique=True, db_index=True)
    patient_id = models.BigIntegerField(unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_number = models.CharField(max_length=10)
    insurance_company = models.ForeignKey(
        "references.InsuranceCompany", on_delete=models.SET_NULL, null=True, blank=True
    )
    insurance_number = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    department_in = models.ForeignKey(
        "references.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients",
    )
    datetime_in = models.DateTimeField(null=True, blank=True)
    datetime_out = models.DateTimeField(null=True, blank=True)
    diagnoses = models.ManyToManyField(
        "references.Diagnosis", through="PatientDiagnosis"
    )
    dekurz_datetime = models.DateTimeField(null=True, blank=True)
    dekurz_who = models.ForeignKey(
        "references.Person", on_delete=models.SET_NULL, null=True, blank=True
    )
    dekurz_department = models.ForeignKey(
        "references.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients_dekurz",
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def update_diagnoses(self, diagnosis) -> None:
        """
        Update diagnoses, but keep diagnosis received via api

        :param diagnosis: list of `Diagnosis` objects
        """
        current_ids = self.diagnoses.values_list("id", flat=True)
        via_api_ids = [
            d.id for d in self.diagnoses.filter(patientdiagnosis__via_api=True)
        ]
        ids_to_keep = [d.id for d in diagnosis] + via_api_ids
        self.diagnoses.exclude(id__in=ids_to_keep).delete()
        for diagnosis in set(filter(lambda d: d.id not in current_ids, diagnosis)):
            self.patientdiagnosis_set.create(patient=self, diagnosis=diagnosis)


class PatientDiagnosis(BaseUpdatableModel):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    diagnosis = models.ForeignKey("references.Diagnosis", on_delete=models.CASCADE)
    via_api = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient} {self.diagnosis}"

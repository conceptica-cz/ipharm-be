from django.db import models
from updates.models import BaseUpdatableModel


class Patient(BaseUpdatableModel):
    clinic = models.ForeignKey("references.Clinic", on_delete=models.CASCADE)
    record_id = models.BigIntegerField(unique=True, db_index=True)
    patient_id = models.BigIntegerField(unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_number = models.CharField(max_length=10)
    insurance_company = models.CharField(max_length=100)
    insurance_number = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    department_in_id = models.IntegerField()
    datetime_in = models.DateTimeField()
    datetime_out = models.DateTimeField(null=True, blank=True)
    diagnosis = models.CharField(max_length=50)
    dekurz_datetime = models.DateTimeField()
    dekurz_who = models.IntegerField()
    dekurz_department = models.IntegerField()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

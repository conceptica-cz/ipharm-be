from django.test import TestCase

from factories.ipharm import PatientFactory


def test_get_medical_procedures_count_for_user(self):
    patient_1 = PatientFactory()
    patient_2 = PatientFactory()

from django.test import TestCase
from ipharm.models import Patient

from factories.ipharm import PatientFactory


class PatientManagerTest(TestCase):
    def test_update_names(self):
        PatientFactory(name="Doe John", first_name=None, last_name=None)
        PatientFactory(name="Smith John", first_name="x", last_name="x")

        Patient.objects.update_names()

        self.assertEqual(Patient.objects.get(name="Doe John").first_name, "John")
        self.assertEqual(Patient.objects.get(name="Doe John").last_name, "Doe")

        self.assertEqual(Patient.objects.get(name="Smith John").first_name, "x")
        self.assertEqual(Patient.objects.get(name="Smith John").last_name, "x")

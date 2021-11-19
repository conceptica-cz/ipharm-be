from django.test import TestCase
from ipharm.models import *

from factories.ipharm import CareFactory, CheckInFactory, PatientFactory
from factories.references import DepartmentFactory


class PatientTest(TestCase):
    def test_create_care(self):
        CheckInFactory()
        print(Patient.objects.all())
        print(Care.objects.all())
        print(CheckIn.objects.all())
        print(CheckIn.objects.first().drugs.all())

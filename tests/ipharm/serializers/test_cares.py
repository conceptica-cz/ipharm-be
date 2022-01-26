from django.test import TestCase
from ipharm.serializers.cares import (
    CareNestedSerializer,
    CareSerializer,
    DekurzNestedSerializer,
)
from references.serializers.clinics import ClinicSerializer, DepartmentSerializer
from references.serializers.diagnoses import DiagnosisSerializer

from factories.ipharm import CareFactory
from factories.references.diagnoses import DiagnosisFactory


class CareNestedSerializerTest(TestCase):
    def setUp(self) -> None:
        self.care = CareFactory()

    def test_clinic_is_nested(self):
        serializer = CareNestedSerializer(instance=self.care)
        clinic_serializer = ClinicSerializer(instance=self.care.clinic)
        self.assertEqual(serializer.data["clinic"], clinic_serializer.data)

    def test_department_is_nested(self):
        serializer = CareNestedSerializer(instance=self.care)
        department_serializer = DepartmentSerializer(instance=self.care.department)
        self.assertEqual(serializer.data["department"], department_serializer.data)

    def test_last_dekurz_is_nested(self):
        serializer = CareNestedSerializer(instance=self.care)
        dekurz_serializer = DekurzNestedSerializer(instance=self.care.last_dekurz)
        self.assertEqual(serializer.data["last_dekurz"], dekurz_serializer.data)


class CareSerializerTest(TestCase):
    def setUp(self) -> None:
        self.care = CareFactory()

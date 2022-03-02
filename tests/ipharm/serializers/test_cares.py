from django.test import TestCase
from ipharm.serializers.cares import (
    CareLiteNestedSerializer,
    CareSerializer,
    DekurzNestedSerializer,
)
from references.serializers.clinics import ClinicSerializer, DepartmentSerializer
from references.serializers.diagnoses import DiagnosisSerializer

from factories.ipharm import CareFactory, PatientFactory
from factories.references import ExternalDepartmentFactory
from factories.references.diagnoses import DiagnosisFactory


class CareNestedSerializerTest(TestCase):
    def setUp(self) -> None:
        self.care = CareFactory()

    def test_clinic_is_nested(self):
        serializer = CareLiteNestedSerializer(instance=self.care)
        clinic_serializer = ClinicSerializer(instance=self.care.clinic)
        self.assertEqual(serializer.data["clinic"], clinic_serializer.data)

    def test_department_is_nested(self):
        serializer = CareLiteNestedSerializer(instance=self.care)
        department_serializer = DepartmentSerializer(instance=self.care.department)
        self.assertEqual(serializer.data["department"], department_serializer.data)

    def test_last_dekurz_is_nested(self):
        serializer = CareLiteNestedSerializer(instance=self.care)
        dekurz_serializer = DekurzNestedSerializer(instance=self.care.last_dekurz)
        self.assertEqual(serializer.data["last_dekurz"], dekurz_serializer.data)


class CareSerializerTest(TestCase):
    def setUp(self) -> None:
        self.patient = PatientFactory()

    def test_external_care__without_external_department(self):
        data = {
            "care_type": "external",
            "patient": self.patient.id,
        }
        serializer = CareSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_external_care__valid_data(self):
        external_department = ExternalDepartmentFactory()
        data = {
            "care_type": "external",
            "patient": self.patient.pk,
            "external_department": external_department.pk,
        }
        serializer = CareSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

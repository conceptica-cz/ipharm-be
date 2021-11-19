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

    def test_diagnoses_is_nested(self):
        serializer = CareNestedSerializer(instance=self.care)
        diagnosis_serializer = DiagnosisSerializer(instance=self.care.diagnoses.first())
        self.assertEqual(serializer.data["diagnoses"], [diagnosis_serializer.data])

    def test_last_dekurz_is_nested(self):
        serializer = CareNestedSerializer(instance=self.care)
        dekurz_serializer = DekurzNestedSerializer(instance=self.care.last_dekurz)
        self.assertEqual(serializer.data["last_dekurz"], dekurz_serializer.data)


class CareSerializerTest(TestCase):
    def setUp(self) -> None:
        self.care = CareFactory()

    def test__update_diagnoses__always_keep_via_api_diagnosis(self):
        """Test that update always keep 'via_api' diagnosis"""
        via_api_diagnosis = self.care.diagnoses.first()
        new_diagnosis_1 = DiagnosisFactory()
        new_diagnosis_2 = DiagnosisFactory()
        new_diagnosis_3 = DiagnosisFactory()
        serializer = CareSerializer(instance=self.care)
        data = serializer.data
        data["diagnoses"] = [
            new_diagnosis_1.id,
            new_diagnosis_2.id,
        ]
        serializer = CareSerializer(instance=self.care, data=data)
        serializer.is_valid()
        serializer.save()

        self.care.refresh_from_db()
        self.assertQuerysetEqual(
            self.care.diagnoses.all(),
            [via_api_diagnosis, new_diagnosis_1, new_diagnosis_2],
            transform=lambda x: x,
            ordered=False,
        )

    def test__update_diagnoses__doesnt_duplicate_diagnoses(self):
        """Test that update doesn't duplicate diagnosis"""
        via_api_diagnosis = self.care.diagnoses.first()
        new_diagnosis_1 = DiagnosisFactory()
        new_diagnosis_2 = DiagnosisFactory()
        serializer = CareSerializer(instance=self.care)
        data = serializer.data
        data["diagnoses"] = [
            via_api_diagnosis.id,
            new_diagnosis_1.id,
            new_diagnosis_2.id,
            new_diagnosis_1.id,
        ]
        serializer = CareSerializer(instance=self.care, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.care.refresh_from_db()
        self.assertQuerysetEqual(
            self.care.diagnoses.all(),
            [via_api_diagnosis, new_diagnosis_1, new_diagnosis_2],
            transform=lambda x: x,
            ordered=False,
        )

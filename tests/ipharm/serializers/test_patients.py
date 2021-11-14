from django.test import TestCase
from ipharm.serializers.patients import PatientNestedSerializer, PatientSerializer
from references.serializers.clinics import DepartmentSerializer
from references.serializers.diagnoses import DiagnosisSerializer
from references.serializers.insurances import InsuranceCompanySerializer
from references.serializers.persons import PersonSerializer

from factories.ipharm.patients import PatientFactory
from factories.references.diagnoses import DiagnosisFactory


class PatientNestedSerializerTest(TestCase):
    def setUp(self) -> None:
        self.patient = PatientFactory()

    def test_insurance_company_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        insurance_company_serializer = InsuranceCompanySerializer(
            instance=self.patient.insurance_company
        )
        self.assertEqual(
            serializer.data["insurance_company"], insurance_company_serializer.data
        )

    def test_department_in_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        department_serializer = DepartmentSerializer(
            instance=self.patient.department_in
        )
        self.assertEqual(serializer.data["department_in"], department_serializer.data)

    def test_dekurz_department_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        department_serializer = DepartmentSerializer(
            instance=self.patient.dekurz_department
        )
        self.assertEqual(
            serializer.data["dekurz_department"], department_serializer.data
        )

    def test_dekurz_who_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        person_serializer = PersonSerializer(instance=self.patient.dekurz_who)
        self.assertEqual(serializer.data["dekurz_who"], person_serializer.data)

    def test_diagnoses_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        diagnosis_serializer = DiagnosisSerializer(
            instance=self.patient.diagnoses.first()
        )
        self.assertEqual(serializer.data["diagnoses"], [diagnosis_serializer.data])


class PatientSerializerTest(TestCase):
    def setUp(self) -> None:
        self.patient = PatientFactory()

    def test__update_diagnoses__always_keep_via_api_diagnosis(self):
        """Test that update always keep 'via_api' diagnosis"""
        via_api_diagnosis = self.patient.diagnoses.first()
        new_diagnosis_1 = DiagnosisFactory()
        new_diagnosis_2 = DiagnosisFactory()
        new_diagnosis_3 = DiagnosisFactory()
        serializer = PatientSerializer(instance=self.patient)
        data = serializer.data
        data["diagnoses"] = [
            new_diagnosis_1.id,
            new_diagnosis_2.id,
        ]
        serializer = PatientSerializer(instance=self.patient, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.patient.refresh_from_db()
        self.assertQuerysetEqual(
            self.patient.diagnoses.all(),
            [via_api_diagnosis, new_diagnosis_1, new_diagnosis_2],
            transform=lambda x: x,
            ordered=False,
        )

    def test__update_diagnoses__doesnt_duplicate_diagnoses(self):
        """Test that update doesn't duplicate diagnosis"""
        via_api_diagnosis = self.patient.diagnoses.first()
        new_diagnosis_1 = DiagnosisFactory()
        new_diagnosis_2 = DiagnosisFactory()
        serializer = PatientSerializer(instance=self.patient)
        data = serializer.data
        data["diagnoses"] = [
            via_api_diagnosis.id,
            new_diagnosis_1.id,
            new_diagnosis_2.id,
            new_diagnosis_1.id,
        ]
        serializer = PatientSerializer(instance=self.patient, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.patient.refresh_from_db()
        self.assertQuerysetEqual(
            self.patient.diagnoses.all(),
            [via_api_diagnosis, new_diagnosis_1, new_diagnosis_2],
            transform=lambda x: x,
            ordered=False,
        )

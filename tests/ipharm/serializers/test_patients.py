import datetime

from django.test import TestCase
from ipharm.models import Care, Patient
from ipharm.serializers.cares import CareNestedSerializer
from ipharm.serializers.patients import PatientNestedSerializer, PatientSerializer
from references.serializers.insurances import InsuranceCompanySerializer

from factories.ipharm import CareFactory
from factories.ipharm.patients import PatientFactory
from factories.references import ClinicFactory, InsuranceCompanyFactory


class PatientNestedSerializerTest(TestCase):
    def setUp(self) -> None:
        self.patient = PatientFactory()
        self.care = CareFactory(patient=self.patient, care_type=Care.HOSPITALIZATION)

    def test_insurance_company_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        insurance_company_serializer = InsuranceCompanySerializer(
            instance=self.patient.insurance_company
        )
        self.assertEqual(
            serializer.data["insurance_company"], insurance_company_serializer.data
        )

    def test_current_care_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        serializer_care = CareNestedSerializer(instance=self.care)
        self.assertEqual(serializer.data["current_care"], serializer_care.data)


class PatientSerializerTest(TestCase):
    def test_create_with_ambulance(self):
        """Test that serializer create both patient and ambulance care"""
        insurance_company = InsuranceCompanyFactory()
        clinic = ClinicFactory()
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime.date(year=1990, month=1, day=1),
            "birth_number": "0000000001",
            "current_care": {
                "care_type": Care.AMBULATION,
                "clinic": clinic.id,
                "external_id": None,
            },
            "insurance_company": insurance_company.id,
            "insurance_number": "42",
        }
        serializer = PatientSerializer(data=data)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        serializer.save()
        patient = Patient.objects.first()
        self.assertEqual(patient.insurance_company, insurance_company)
        self.assertEqual(patient.insurance_number, "42")
        ambulance_care = Care.objects.get(patient=patient, care_type=Care.AMBULATION)
        self.assertEqual(ambulance_care.clinic, clinic)
        self.assertEqual(patient.current_care, ambulance_care)

    def test_create_with_hospital(self):
        """Test that serializer create both patient and hospital care"""
        insurance_company = InsuranceCompanyFactory()
        clinic = ClinicFactory()
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime.date(year=1990, month=1, day=1),
            "birth_number": "0000000001",
            "current_care": {
                "care_type": Care.HOSPITALIZATION,
                "clinic": clinic.id,
                "external_id": None,
            },
            "insurance_company": insurance_company.id,
            "insurance_number": "42",
        }
        serializer = PatientSerializer(data=data)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        patient = serializer.save()
        self.assertEqual(patient.insurance_company, insurance_company)
        self.assertEqual(patient.insurance_number, "42")
        hospital_care = Care.objects.get(
            patient=patient, care_type=Care.HOSPITALIZATION
        )
        self.assertEqual(hospital_care.clinic, clinic)
        self.assertEqual(patient.current_care, hospital_care)

    def test_update_existing_ambulance(self):
        """Test that serializer updates both patient and ambulance care"""
        patient = PatientFactory(birth_number="1")
        clinic = ClinicFactory()
        care = CareFactory(patient=patient, care_type=Care.AMBULATION, clinic=clinic)
        new_clinic = ClinicFactory()
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime.date(year=1990, month=1, day=1),
            "birth_number": "2",
            "current_care": {
                "clinic": new_clinic.id,
                "external_id": None,
            },
        }
        serializer = PatientSerializer(instance=patient, data=data)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        serializer.save()
        patient.refresh_from_db()
        self.assertEqual(patient.birth_number, "2")
        care.refresh_from_db()
        self.assertEqual(care.clinic, new_clinic)

    def test_update_new_ambulance(self):
        """Test that serializer updates patient and creates ambulance care"""
        patient = PatientFactory(birth_number="1")
        clinic = ClinicFactory()
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime.date(year=1990, month=1, day=1),
            "birth_number": "2",
            "current_care": {
                "care_type": Care.AMBULATION,
                "clinic": clinic.id,
                "external_id": None,
            },
        }
        serializer = PatientSerializer(instance=patient, data=data)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        serializer.save()
        patient.refresh_from_db()
        self.assertEqual(patient.birth_number, "2")
        care = Care.objects.get(patient=patient, care_type=Care.AMBULATION)
        self.assertEqual(care.clinic, clinic)

    def test_update_existing_hospital(self):
        """Test that serializer updates both patient and hospital care"""
        patient = PatientFactory(birth_number="1")
        clinic = ClinicFactory()
        care = CareFactory(
            patient=patient, care_type=Care.HOSPITALIZATION, clinic=clinic
        )
        new_clinic = ClinicFactory()
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime.date(year=1990, month=1, day=1),
            "birth_number": "2",
            "current_care": {
                "care_type": Care.HOSPITALIZATION,
                "clinic": new_clinic.id,
                "external_id": None,
            },
        }
        serializer = PatientSerializer(instance=patient, data=data)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        serializer.save()
        patient.refresh_from_db()
        self.assertEqual(patient.birth_number, "2")
        care.refresh_from_db()
        self.assertEqual(care.clinic, new_clinic)

    def test_update_new_hospital(self):
        """Test that serializer updates patient and creates hospital care"""
        patient = PatientFactory(birth_number="1")
        clinic = ClinicFactory()
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime.date(year=1990, month=1, day=1),
            "birth_number": "2",
            "current_care": {
                "care_type": Care.HOSPITALIZATION,
                "clinic": clinic.id,
                "external_id": None,
            },
        }
        serializer = PatientSerializer(instance=patient, data=data)

        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        serializer.save()
        patient.refresh_from_db()
        self.assertEqual(patient.birth_number, "2")
        care = Care.objects.get(patient=patient, care_type=Care.HOSPITALIZATION)
        self.assertEqual(care.clinic, clinic)

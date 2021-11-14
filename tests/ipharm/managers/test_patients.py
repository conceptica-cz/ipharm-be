from datetime import datetime

from django.test import TestCase
from ipharm.models import Patient, PatientDiagnosis
from references.models import Clinic, Diagnosis
from updates.transformers import delete_id

from factories.ipharm.patients import PatientFactory
from factories.references.clinics import ClinicFactory
from factories.references.diagnoses import DiagnosisFactory


class BestUpdatableManagerTest(TestCase):
    """Test creating/getting related instances"""

    def test_update_or_create_from_dict__new_related_instance(self):
        """Test that new instance is created"""
        identifiers = ["patient_id", "patient_type"]
        relations = {
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            }
        }
        data = {
            "id": 172,
            "clinic_identifier": 42,
            "patient_type": "hospital",
            "record_id": 3,
            "patient_id": 4,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
        }
        patient, operation = Patient.objects.update_or_create_from_dict(
            identifiers=identifiers,
            data=data,
            relations=relations,
            transformer=delete_id,
        )

        self.assertEqual(Patient.objects.count(), 1)

        expected = Patient.objects.get(patient_id=4)
        self.assertEqual(patient, expected)
        self.assertEqual(operation, Patient.objects.CREATED)

        self.assertEqual(Clinic.objects.count(), 1)
        self.assertEqual(patient.clinic.identifier, 42)
        self.assertEqual(patient.clinic.description, "TMP")

    def test_update_or_create_from_dict__existing_related_instance(self):
        """Test that existing instances used as related"""
        existing_clinic = ClinicFactory(identifier=42)
        identifiers = ["patient_id", "patient_type"]
        relations = {
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            }
        }
        data = {
            "id": 172,
            "clinic_identifier": 42,
            "patient_type": "hospital",
            "record_id": 3,
            "patient_id": 4,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
        }
        patient, operation = Patient.objects.update_or_create_from_dict(
            identifiers=identifiers,
            data=data,
            relations=relations,
            transformer=delete_id,
        )

        self.assertEqual(Patient.objects.count(), 1)

        expected = Patient.objects.get(patient_id=4)
        self.assertEqual(patient, expected)
        self.assertEqual(operation, Patient.objects.CREATED)

        self.assertEqual(Clinic.objects.count(), 1)
        self.assertEqual(patient.clinic, existing_clinic)

    def test_update_or_create_from_dict__new_many_to_many_instance(self):
        """Test that new many to many instance is created"""
        identifiers = ["patient_id", "patient_type"]
        relations = {
            "diagnosis": {"field": "diagnoses", "key": "code"},
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            },
        }
        data = {
            "id": 172,
            "clinic_identifier": 42,
            "patient_type": "hospital",
            "record_id": 3,
            "patient_id": 4,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
            "diagnosis": 48,
        }
        patient, operation = Patient.objects.update_or_create_from_dict(
            identifiers=identifiers,
            data=data,
            relations=relations,
            transformer=delete_id,
        )

        self.assertEqual(Patient.objects.count(), 1)

        expected = Patient.objects.get(patient_id=4)
        self.assertEqual(patient, expected)
        self.assertEqual(operation, Patient.objects.CREATED)

        self.assertEqual(Diagnosis.objects.count(), 1)
        self.assertEqual(patient.diagnoses.first().code, "48")

    def test_update_or_create_from_dict__existing_patient__update_many_to_many_instance(
        self,
    ):
        """Test that existing instances used as related"""
        diagnosis_manual_1 = DiagnosisFactory(code="41")
        diagnosis_manual_2 = DiagnosisFactory(code="42")

        initial_patient = PatientFactory()
        diagnosis_via_api = initial_patient.diagnoses.first()
        diagnosis_via_api.code_id = "39"
        diagnosis_via_api.save()
        initial_patient.diagnoses.add(diagnosis_manual_1)
        initial_patient.diagnoses.add(diagnosis_manual_2)
        initial_patient.save()
        self.assertEqual(Diagnosis.objects.count(), 3)

        PatientDiagnosis(
            patient=initial_patient, diagnosis=diagnosis_via_api, via_api=True
        )
        PatientDiagnosis(
            patient=initial_patient, diagnosis=diagnosis_manual_1, via_api=False
        )
        PatientDiagnosis(
            patient=initial_patient, diagnosis=diagnosis_manual_2, via_api=False
        )

        identifiers = ["patient_id", "patient_type"]
        relations = {
            "diagnosis": {"field": "diagnoses", "key": "code"},
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            },
        }
        data = {
            "id": 172,
            "clinic_identifier": 42,
            "patient_type": initial_patient.patient_type,
            "record_id": 3,
            "patient_id": initial_patient.patient_id,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
            "diagnosis": 40,
        }
        patient, operation = Patient.objects.update_or_create_from_dict(
            identifiers=identifiers,
            data=data,
            relations=relations,
            transformer=delete_id,
        )

        self.assertEqual(Patient.objects.count(), 1)

        self.assertEqual(patient, initial_patient)
        self.assertEqual(operation, Patient.objects.UPDATED)

        self.assertEqual(Diagnosis.objects.count(), 4)
        self.assertEqual(patient.diagnoses.count(), 3)

        self.assertIn(diagnosis_manual_1, patient.diagnoses.all())
        self.assertIn(diagnosis_manual_2, patient.diagnoses.all())
        self.assertNotIn(initial_patient, patient.diagnoses.all())

    def test_not_changed_object__not_changed(self):
        """Test that _not_changed_object return object if object was not changed"""
        relations = {
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            }
        }
        data = {
            "clinic_identifier": 42,
            "patient_type": "hospital",
            "record_id": 3,
            "patient_id": 4,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
        }
        clinic = ClinicFactory(identifier=42)
        patient = PatientFactory(
            patient_id=4,
            patient_type="hospital",
            record_id=3,
            first_name="John",
            last_name="Doe",
            birth_date=datetime(1980, 1, 1),
            birth_number="123456789",
            height=120,
            weight=80,
            clinic=clinic,
            insurance_company=None,
            department_in=None,
            datetime_in=None,
            datetime_out=None,
        )
        not_changed = Patient.objects._not_changed_object(data, relations)
        self.assertEqual(not_changed, patient)

    def test_not_changed_object__casual_field_changed(self):
        """Test that _not_changed_object returns None if casual field changed"""
        relations = {
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            }
        }
        data = {
            "clinic_identifier": 42,
            "patient_type": "hospital",
            "record_id": 39,  # changed
            "patient_id": 4,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
        }
        clinic = ClinicFactory(identifier=42)
        patient = PatientFactory(
            patient_id=4,
            patient_type="hospital",
            record_id=3,
            first_name="John",
            last_name="Doe",
            birth_date=datetime(1980, 1, 1),
            birth_number="123456789",
            height=120,
            weight=80,
            clinic=clinic,
            insurance_company=None,
            department_in=None,
            datetime_in=None,
            datetime_out=None,
        )
        not_changed = Patient.objects._not_changed_object(data, relations)
        self.assertEqual(not_changed, None)

    def test_not_changed_object__many_to_one_changed(self):
        """Test that _not_changed_object returns None if many to one field changed"""
        relations = {
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            }
        }
        data = {
            "clinic_identifier": 43,
            "patient_type": "hospital",
            "record_id": 3,
            "patient_id": 4,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
        }
        clinic_42 = ClinicFactory(identifier=42)
        clinic_43 = ClinicFactory(identifier=43)
        patient = PatientFactory(
            patient_id=4,
            patient_type="hospital",
            record_id=3,
            first_name="John",
            last_name="Doe",
            birth_date=datetime(1980, 1, 1),
            birth_number="123456789",
            height=120,
            weight=80,
            clinic=clinic_42,
            insurance_company=None,
            department_in=None,
            datetime_in=None,
            datetime_out=None,
        )
        not_changed = Patient.objects._not_changed_object(data, relations)
        self.assertEqual(not_changed, None)

    def test_not_changed_object__many_to_many_considered_unchanged(self):
        """
        Test that _not_changed_object returns object if many to many field not changed
        Only the `via_api` objects must be taken into account.
        """
        relations = {
            "diagnosis": {"field": "diagnoses", "key": "code"},
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            },
        }
        data = {
            "clinic_identifier": 42,
            "patient_type": "hospital",
            "record_id": 3,
            "patient_id": 4,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
            "diagnosis": 39,
        }
        clinic = ClinicFactory(identifier=42)
        patient = PatientFactory(
            patient_id=4,
            patient_type="hospital",
            record_id=3,
            first_name="John",
            last_name="Doe",
            birth_date=datetime(1980, 1, 1),
            birth_number="123456789",
            height=120,
            weight=80,
            clinic=clinic,
            insurance_company=None,
            department_in=None,
            datetime_in=None,
            datetime_out=None,
        )
        diagnosis_manual_1 = DiagnosisFactory(code="41")
        diagnosis_manual_2 = DiagnosisFactory(code="42")

        diagnosis_via_api = patient.diagnoses.first()
        diagnosis_via_api.code = "39"
        diagnosis_via_api.save()
        patient.diagnoses.add(diagnosis_manual_1)
        patient.diagnoses.add(diagnosis_manual_2)
        patient.save()

        # the patient.diagnoses = [39, 41, 42]
        # data.diagnoses = 39
        # but because we take in account only the via_api objects (39),
        # the patient is considered unchanged

        not_changed = Patient.objects._not_changed_object(data, relations)
        self.assertEqual(not_changed, patient)

    def test_not_changed_object__many_to_many_changed(self):
        """Test that _not_changed_object returns None if many to many field changed"""
        relations = {
            "diagnosis": {"field": "diagnoses", "key": "code"},
            "clinic_identifier": {
                "field": "clinic",
                "key": "identifier",
                "delete_source_field": True,
            },
        }
        data = {
            "clinic_identifier": 42,
            "patient_type": "hospital",
            "record_id": 3,
            "patient_id": 4,
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": datetime(1980, 1, 1),
            "birth_number": "123456789",
            "insurance_company": None,
            "height": 120,
            "weight": 80,
            "department_in": None,
            "datetime_in": None,
            "datetime_out": None,
            "diagnosis": 39,
        }
        clinic = ClinicFactory(identifier=42)
        patient = PatientFactory(
            patient_id=4,
            patient_type="hospital",
            record_id=3,
            first_name="John",
            last_name="Doe",
            birth_date=datetime(1980, 1, 1),
            birth_number="123456789",
            height=120,
            weight=80,
            clinic=clinic,
            insurance_company=None,
            department_in=None,
            datetime_in=None,
            datetime_out=None,
        )
        diagnosis_via_api = patient.diagnoses.first()
        diagnosis_via_api.code = "40"
        diagnosis_via_api.save()
        not_changed = Patient.objects._not_changed_object(data, relations)
        self.assertEqual(not_changed, None)

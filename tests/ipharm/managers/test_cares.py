from datetime import datetime

from django.test import TestCase
from ipharm.models import Care, Patient
from references.models import Clinic, Diagnosis
from updates.transformers import delete_id

from factories.ipharm.cares import CareFactory, PatientFactory
from factories.references.clinics import ClinicFactory
from factories.references.diagnoses import DiagnosisFactory


class BestUpdatableManagerTest(TestCase):
    """Test creating/getting related instances"""

    def setUp(self) -> None:
        self.patient = PatientFactory()

    def test_update_or_create_from_dict__new_related_instance(self):
        """Test that new instance is created"""
        identifiers = ["external_id"]
        relations = {
            "clinic_external_id": {
                "field": "clinic",
                "key": "external_id",
                "delete_source_field": True,
            },
            "patient_external_id": {
                "field": "patient",
                "key": "external_id",
                "delete_source_field": True,
            },
        }
        data = {
            "id": 172,
            "patient_external_id": self.patient.external_id,
            "clinic_external_id": 42,
            "care_type": "hospitalization",
            "external_id": 3,
        }
        care, operation = Care.objects.update_or_create_from_dict(
            identifiers=identifiers,
            data=data,
            relations=relations,
            transformer=delete_id,
        )

        self.assertEqual(Care.objects.count(), 1)

        expected = Care.objects.get(external_id=3)
        self.assertEqual(care, expected)
        self.assertEqual(operation, Care.objects.CREATED)

        self.assertEqual(Clinic.objects.count(), 1)
        self.assertEqual(care.clinic.external_id, 42)
        self.assertEqual(care.clinic.description, "TMP")
        self.assertEqual(care.patient, self.patient)

    def test_update_or_create_from_dict__existing_related_instance(self):
        """Test that existing instances used as related"""
        existing_clinic = ClinicFactory(external_id=42)
        identifiers = ["external_id"]
        relations = {
            "clinic_external_id": {
                "field": "clinic",
                "key": "external_id",
                "delete_source_field": True,
            },
            "patient_external_id": {
                "field": "patient",
                "key": "external_id",
                "delete_source_field": True,
            },
        }
        data = {
            "id": 172,
            "patient_external_id": self.patient.external_id,
            "clinic_external_id": 42,
            "care_type": "hospitalization",
            "external_id": 3,
        }
        care, operation = Care.objects.update_or_create_from_dict(
            identifiers=identifiers,
            data=data,
            relations=relations,
            transformer=delete_id,
        )

        self.assertEqual(Care.objects.count(), 1)

        expected = Care.objects.get(external_id=3)
        self.assertEqual(care, expected)
        self.assertEqual(operation, Care.objects.CREATED)

        self.assertEqual(Clinic.objects.count(), 1)
        self.assertEqual(care.clinic, existing_clinic)

    def test_is_changed__not_changed(self):
        """Test that _not_changed_object return object if object was not changed"""
        relations = {
            "clinic_external_id": {
                "field": "clinic",
                "key": "external_id",
                "delete_source_field": True,
            },
            "patient_external_id": {
                "field": "patient",
                "key": "external_id",
                "delete_source_field": True,
            },
        }
        data = {
            "patient_external_id": self.patient.external_id,
            "clinic_external_id": 42,
            "care_type": "hospitalization",
            "external_id": 4,
        }
        clinic = ClinicFactory(external_id=42)
        care = CareFactory(
            patient=self.patient,
            external_id=4,
            care_type="hospitalization",
            clinic=clinic,
        )

        obj, changed = Care.objects._is_changed(data, relations)
        self.assertEqual(changed, False)
        self.assertEqual(obj, care)

    def test_is_changed__casual_field_changed(self):
        """Test that _not_changed_object returns None if casual field changed"""
        relations = {
            "clinic_external_id": {
                "field": "clinic",
                "key": "external_id",
                "delete_source_field": True,
            },
            "patient_external_id": {
                "field": "patient",
                "key": "external_id",
                "delete_source_field": True,
            },
        }
        data = {
            "patient_external_id": self.patient.external_id,
            "clinic_external_id": 42,
            "care_type": "hospitalization",
            "external_id": 3,  # changed
        }
        clinic = ClinicFactory(external_id=42)
        care = CareFactory(
            patient=self.patient,
            external_id=4,
            care_type="hospitalization",
            clinic=clinic,
        )
        obj, changed = Care.objects._is_changed(data, relations)
        self.assertEqual(changed, True)

    def test_is_changed__many_to_one_changed(self):
        """Test that _not_changed_object returns None if many to one field changed"""
        relations = {
            "clinic_external_id": {
                "field": "clinic",
                "key": "external_id",
                "delete_source_field": True,
            },
            "patient_external_id": {
                "field": "patient",
                "key": "external_id",
                "delete_source_field": True,
            },
        }
        data = {
            "patient_external_id": self.patient.external_id,
            "clinic_external_id": 43,
            "care_type": "hospitalization",
            "external_id": 4,
        }
        clinic_42 = ClinicFactory(external_id=42)
        clinic_43 = ClinicFactory(external_id=43)
        care = CareFactory(
            patient=self.patient,
            external_id=4,
            care_type="hospitalization",
            clinic=clinic_42,
        )
        obj, changed = Care.objects._is_changed(data, relations)
        self.assertEqual(changed, True)

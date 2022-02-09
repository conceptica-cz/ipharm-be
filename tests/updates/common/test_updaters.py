from django.test import TestCase
from references.models import Clinic, Department
from updates.common.updaters import simple_model_updater

from factories.references import ClinicFactory


class SimpleModelUpdaterTestCase(TestCase):
    """
    Test case for the simple_model_updater.
    """

    def test_create_new_without_relations(self):
        """Test that new instance is created"""
        ClinicFactory(external_id=42)
        identifiers = ["external_id"]
        data = {
            "external_id": 43,
            "abbreviation": "AMB",
            "description": "Ambulance",
            "is_hospital": True,
            "is_ambulance": True,
        }
        result = simple_model_updater(
            data=data, model="references.Clinic", identifiers=identifiers
        )

        self.assertEqual(result, {"references.Clinic": "created"})
        self.assertEqual(Clinic.objects.count(), 2)

        expected = Clinic.objects.get(external_id=43)
        self.assertEqual(expected.abbreviation, "AMB")
        self.assertEqual(expected.description, "Ambulance")

    def test_update_existing_without_relations(self):
        """Test that new instance is created"""
        ClinicFactory(external_id=42)
        identifiers = ["external_id"]
        data = {
            "external_id": 42,
            "abbreviation": "AMB",
            "description": "Ambulance",
            "is_hospital": True,
            "is_ambulance": True,
        }
        result = simple_model_updater(
            data=data, model="references.Clinic", identifiers=identifiers
        )

        self.assertEqual(result, {"references.Clinic": "updated"})
        self.assertEqual(Clinic.objects.count(), 1)

        expected = Clinic.objects.get(external_id=42)
        self.assertEqual(expected.abbreviation, "AMB")
        self.assertEqual(expected.description, "Ambulance")

    def test_create_new_with_relations(self):
        """Test that new instance is created"""
        clinic = ClinicFactory(external_id=42)
        identifiers = ["external_id"]
        data = {
            "external_id": 2,
            "abbreviation": "D1",
            "description": "Department_1",
            "clinic_external_id": 42,
        }
        result = simple_model_updater(
            data=data,
            model="references.Department",
            identifiers=identifiers,
            relations={
                "clinic_external_id": {
                    "field": "clinic",
                    "key": "external_id",
                    "delete_source_field": True,
                }
            },
        )

        self.assertEqual(result, {"references.Department": "created"})
        self.assertEqual(Clinic.objects.count(), 1)

        expected = Department.objects.get(external_id=2)
        self.assertEqual(expected.abbreviation, "D1")
        self.assertEqual(expected.clinic, clinic)

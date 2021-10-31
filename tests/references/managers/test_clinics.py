from django.test import TestCase
from references.models import Clinic
from updates.transformers import delete_id

from factories.references.clinics import AmbulanceFactory, ClinicFactory
from factories.updates.updates import ReferenceUpdateFactory
from factories.users import UserFactory


class ClinicManagerTest(TestCase):
    def test_update_or_create_from_dict__new(self):
        """Test that new instance is created"""
        ClinicFactory(clinic_id=42)
        AmbulanceFactory(clinic_id=42)
        identifiers = ["clinic_type", "clinic_id"]
        data = {
            "clinic_type": Clinic.AMBULANCE,
            "clinic_id": 43,
            "abbreviation": "AMB",
            "description": "Ambulance",
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(
            identifiers=identifiers, data=data, transformer=delete_id
        )

        self.assertEqual(Clinic.objects.count(), 3)

        expected = Clinic.objects.get(clinic_id=43)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.CREATED)
        self.assertEqual(expected.clinic_type, Clinic.AMBULANCE)
        self.assertEqual(expected.abbreviation, "AMB")
        self.assertEqual(expected.description, "Ambulance")

    def test_update_or_create_from_dict__existing(self):
        """Test that existing instance that have differences is updated"""
        ClinicFactory(clinic_id=42)
        AmbulanceFactory(clinic_id=43)
        ClinicFactory(
            clinic_id=43,
            clinic_type=Clinic.CLINIC,
            abbreviation="CL",
            description="Clinic",
        )
        identifiers = ["clinic_type", "clinic_id"]
        data = {
            "clinic_type": Clinic.CLINIC,
            "clinic_id": 43,
            "abbreviation": "CLN",
            "description": "Clinic new",
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(identifiers, data)

        self.assertEqual(Clinic.objects.count(), 3)

        expected = Clinic.objects.get(clinic_id=43, clinic_type=Clinic.CLINIC)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.UPDATED)
        self.assertEqual(expected.abbreviation, "CLN")
        self.assertEqual(expected.description, "Clinic new")

    def test_update_or_create_from_dict__existing_without_difference(self):
        """Test that existing instance that have differences is updated"""
        ClinicFactory(clinic_id=42)
        AmbulanceFactory(clinic_id=43)
        ClinicFactory(
            clinic_id=43,
            clinic_type=Clinic.CLINIC,
            abbreviation="CL",
            description="Clinic",
        )
        identifiers = ["clinic_type", "clinic_id"]
        data = {
            "clinic_type": Clinic.CLINIC,
            "clinic_id": 43,
            "abbreviation": "CL",
            "description": "Clinic",
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(identifiers, data)

        self.assertEqual(Clinic.objects.count(), 3)

        expected = Clinic.objects.get(clinic_id=43, clinic_type=Clinic.CLINIC)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.NOT_CHANGED)
        self.assertEqual(expected.abbreviation, "CL")
        self.assertEqual(expected.description, "Clinic")

    def test_update_or_create_from_dict__set_history_user(self):
        """Test that method (optionally) set history user"""
        user = UserFactory(username="updater")
        identifiers = ["clinic_type", "clinic_id"]
        data = {
            "clinic_type": Clinic.CLINIC,
            "clinic_id": 43,
            "abbreviation": "CLN",
            "description": "Clinic new",
        }

        clinic, _ = Clinic.objects.update_or_create_from_dict(
            identifiers, data, user=user
        )

        history = clinic.history.first()
        self.assertEqual(history.history_user, user)

    def test_update_or_create_from_dict__set_update_attribute(self):
        """Test that method (optionally) set update attribute"""
        user = UserFactory(username="updater")
        identifiers = ["clinic_type", "clinic_id"]
        data = {
            "clinic_type": Clinic.CLINIC,
            "clinic_id": 43,
            "abbreviation": "CLN",
            "description": "Clinic new",
        }
        update = ReferenceUpdateFactory()

        clinic, _ = Clinic.objects.update_or_create_from_dict(
            identifiers, data, user=user, update=update
        )

        history = clinic.history.first()
        self.assertEqual(history.history_user, user)

from django.test import TestCase
from references.models import Clinic
from updates.transformers import delete_id

from factories.references.clinics import ClinicFactory
from factories.updates.updates import ReferenceUpdateFactory
from factories.users import UserFactory


class BestUpdatableManagerTest(TestCase):
    def test_update_or_create_from_dict__new(self):
        """Test that new instance is created"""
        ClinicFactory(clinic_id=42)
        identifiers = ["clinic_id"]
        data = {
            "clinic_id": 43,
            "abbreviation": "AMB",
            "description": "Ambulance",
            "is_hospital": True,
            "is_ambulance": True,
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(
            identifiers=identifiers, data=data, transformer=delete_id
        )

        self.assertEqual(Clinic.objects.count(), 2)

        expected = Clinic.objects.get(clinic_id=43)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.CREATED)
        self.assertEqual(expected.abbreviation, "AMB")
        self.assertEqual(expected.description, "Ambulance")

    def test_update_or_create_from_dict__existing(self):
        """Test that existing instance that have differences is updated"""
        ClinicFactory(
            clinic_id=42,
            abbreviation="CL",
            description="Clinic",
        )
        identifiers = ["clinic_id"]
        data = {
            "clinic_id": 42,
            "abbreviation": "CLN",
            "description": "Clinic new",
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(identifiers, data)

        self.assertEqual(Clinic.objects.count(), 1)

        expected = Clinic.objects.get(clinic_id=42)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.UPDATED)
        self.assertEqual(expected.abbreviation, "CLN")
        self.assertEqual(expected.description, "Clinic new")

    def test_update_or_create_from_dict__existing_without_difference(self):
        """Test that existing instance that have differences is updated"""
        ClinicFactory(
            clinic_id=42,
            abbreviation="CL",
            description="Clinic",
        )
        identifiers = ["clinic_id"]
        data = {
            "clinic_id": 42,
            "abbreviation": "CL",
            "description": "Clinic",
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(identifiers, data)

        self.assertEqual(Clinic.objects.count(), 1)

        expected = Clinic.objects.get(clinic_id=42)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.NOT_CHANGED)
        self.assertEqual(expected.abbreviation, "CL")
        self.assertEqual(expected.description, "Clinic")

    def test_update_or_create_from_dict__set_history_user(self):
        """Test that method (optionally) set history user"""
        user = UserFactory(username="updater")
        identifiers = ["clinic_id"]
        data = {
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
        identifiers = ["clinic_id"]
        data = {
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


class ClinicManagerTest(TestCase):
    def setUp(self) -> None:
        self.hospital_1 = ClinicFactory(is_hospital=True, is_ambulance=False)
        self.hospital_2 = ClinicFactory(is_hospital=True, is_ambulance=False)
        self.ambulance_1 = ClinicFactory(is_hospital=False, is_ambulance=True)
        self.ambulance_2 = ClinicFactory(is_hospital=False, is_ambulance=True)
        self.both_1 = ClinicFactory(is_hospital=True, is_ambulance=True)
        self.both_2 = ClinicFactory(is_hospital=True, is_ambulance=True)

        self.user = UserFactory()
        self.user.hospitals.add(self.hospital_1, self.both_1)
        self.user.ambulances.add(self.ambulance_1, self.both_1, self.both_2)
        self.user.save()

    def test_get_my_hospitals(self):
        clinics = Clinic.objects.get_my_hospitals(user=self.user)

        self.assertQuerysetEqual(
            clinics,
            [self.hospital_1, self.both_1],
            transform=lambda c: c,
            ordered=False,
        )

    def test_get_my_ambulances(self):
        clinics = Clinic.objects.get_my_ambulances(user=self.user)

        self.assertQuerysetEqual(
            clinics,
            [self.ambulance_1, self.both_1, self.both_2],
            transform=lambda c: c,
            ordered=False,
        )

    def test_get_hospitals(self):
        clinics = Clinic.objects.get_hospitals()

        self.assertQuerysetEqual(
            clinics,
            [self.hospital_1, self.hospital_2, self.both_1, self.both_2],
            transform=lambda c: c,
            ordered=False,
        )

    def test_get_ambulances(self):
        clinics = Clinic.objects.get_ambulances()

        self.assertQuerysetEqual(
            clinics,
            [self.ambulance_1, self.ambulance_2, self.both_1, self.both_2],
            transform=lambda c: c,
            ordered=False,
        )

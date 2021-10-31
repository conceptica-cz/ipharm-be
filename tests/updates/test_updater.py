from unittest.mock import Mock, call, patch

from django.test import TestCase, override_settings
from django.utils import timezone
from references.models import Clinic
from updates.transformers import delete_id
from updates.updater import ReferenceSettings, Updater, get_data

from factories.references.clinics import AmbulanceFactory, ClinicFactory


class ReferenceSettingsTest(TestCase):
    def test_model_class(self):
        self.reference = ReferenceSettings("Clinic")
        self.assertEqual(self.reference.model_class, Clinic)

    def test_transformer(self):
        self.reference = ReferenceSettings("Clinic")
        self.assertEqual(self.reference.transformer, delete_id)

    def test_identifiers(self):
        self.reference = ReferenceSettings("Clinic")
        self.assertEqual(self.reference.identifiers, ["clinic_type", "clinic_id"])

    @override_settings(BASE_REFERENCES_URL="http://localhost")
    def test_url(self):
        self.reference = ReferenceSettings("Clinic")
        self.assertEqual(self.reference.url, "http://localhost/clinics/")


class GetDataTest(TestCase):
    @patch("updates.updater.requests.get")
    def test__result__for_single_page(self, mocked_get: Mock):
        mocked_get.side_effect = [
            Mock(json=Mock(return_value={"results": ["result1", "result2", "result3"]}))
        ]

        results = list(get_data("url"))

        self.assertEqual(results, ["result1", "result2", "result3"])

    @patch("updates.updater.requests.get")
    def test_read_all_pages(self, mocked_get: Mock):
        """Test if read all page for paginated result"""
        mocked_get.side_effect = [
            Mock(
                json=Mock(
                    return_value={
                        "count": 5,
                        "next": "http://example.com/api/items/?limit=2&offset=2",
                        "previous": None,
                        "results": ["result1", "result2"],
                    }
                )
            ),
            Mock(
                json=Mock(
                    return_value={
                        "count": 5,
                        "next": "http://example.com/api/items/?limit=2&offset=4",
                        "previous": "http://example.com/api/items/?limit=2",
                        "results": ["result3", "result4"],
                    }
                )
            ),
            Mock(
                json=Mock(
                    return_value={
                        "count": 5,
                        "next": None,
                        "previous": "http://example.com/api/items/?limit=2&offset=2",
                        "results": ["result5"],
                    }
                )
            ),
        ]

        results = list(get_data(url="http://example.com/api/items/"))

        self.assertEqual(
            results, ["result1", "result2", "result3", "result4", "result5"]
        )


class UpdaterTest(TestCase):
    def test_init__set_attributes(self):
        updater = Updater("Clinic")
        self.assertEqual(updater.reference_settings.model_class, Clinic)
        self.assertEqual(updater.reference.model, "Clinic")

    @patch("updates.models.timezone.now")
    @patch("updates.updater.get_data")
    def test_update__create_new_reference_update_instance(
        self, mocked_get_data: Mock, mocked_now: Mock
    ):
        mocked_get_data.return_value = []
        now = timezone.datetime(2021, 10, 1, tzinfo=timezone.utc)
        mocked_now.return_value = now

        updater = Updater("Clinic")
        updater.update()

        reference_update = updater.reference.referenceupdate_set.first()
        self.assertEqual(reference_update.started_at, now)

    @patch("updates.updater.get_data")
    def test_update__update_reference_model(self, mocked_get_data: Mock):
        """Tests that update create and update models"""
        ClinicFactory(clinic_id=1, clinic_type=Clinic.CLINIC, abbreviation="C1")
        AmbulanceFactory(clinic_id=1, clinic_type=Clinic.AMBULANCE, abbreviation="AMB")
        api_data = [
            {
                "id": 42,
                "clinic_type": "clinic",
                "clinic_id": 1,
                "abbreviation": "CL1",
                "description": "Clinica 1",
            },
            {
                "id": 42,
                "clinic_type": "clinic",
                "clinic_id": 2,
                "abbreviation": "CL2",
                "description": "Clinica 2",
            },
            {
                "id": 42,
                "clinic_type": "clinic",
                "clinic_id": 3,
                "abbreviation": "CL3",
                "description": "Clinica 3",
            },
        ]
        mocked_get_data.return_value = api_data
        updater = Updater("Clinic")
        updater.update()

        self.assertEqual(Clinic.objects.count(), 4)

        ambulance = Clinic.objects.get(clinic_id=1, clinic_type=Clinic.AMBULANCE)
        clinic_1 = Clinic.objects.get(clinic_id=1, clinic_type=Clinic.CLINIC)
        clinic_2 = Clinic.objects.get(clinic_id=2, clinic_type=Clinic.CLINIC)
        clinic_3 = Clinic.objects.get(clinic_id=3, clinic_type=Clinic.CLINIC)
        self.assertEqual(ambulance.abbreviation, "AMB")
        self.assertEqual(clinic_1.abbreviation, "CL1")
        self.assertEqual(clinic_2.abbreviation, "CL2")
        self.assertEqual(clinic_3.abbreviation, "CL3")

        reference_update = updater.reference_update
        reference_update.refresh_from_db()
        self.assertEqual(reference_update.created, 2)
        self.assertEqual(reference_update.updated, 1)

    @patch("updates.updater.get_data")
    def test_update__set_history_attributes(self, mocked_get_data: Mock):
        """Tests that update history attributes - user and update"""
        ClinicFactory(clinic_id=1, clinic_type=Clinic.CLINIC, abbreviation="C1")
        api_data = [
            {
                "id": 42,
                "clinic_type": "clinic",
                "clinic_id": 1,
                "abbreviation": "CL1",
                "description": "Clinica 1",
            },
            {
                "id": 42,
                "clinic_type": "clinic",
                "clinic_id": 2,
                "abbreviation": "CL2",
                "description": "Clinica 2",
            },
        ]
        mocked_get_data.return_value = api_data
        updater = Updater("Clinic")
        updater.update()

        clinic_1 = Clinic.objects.get(clinic_id=1, clinic_type=Clinic.CLINIC)
        clinic_2 = Clinic.objects.get(clinic_id=2, clinic_type=Clinic.CLINIC)

        history_1 = clinic_1.history.first()
        history_user_1 = history_1.history_user
        history_2 = clinic_2.history.first()
        history_user_2 = history_2.history_user

        self.assertEqual(history_user_1.username, "updater")
        self.assertEqual(history_1.update, updater.reference_update)

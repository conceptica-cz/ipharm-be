from unittest import TestCase
from unittest.mock import Mock, call

from django.conf import settings
from django.test import TestCase as DjangoTestCase
from django.test import override_settings
from references.models import Clinic
from updates.common.loaders import references_loader
from updates.common.transformers import delete_id
from updates.common.updaters import simple_model_updater
from updates.updater import Updater, UpdaterFactory

from factories.references.clinics import ClinicFactory


class UpdaterTest(DjangoTestCase):
    def test_update_calculates_results__single_model(self):
        data_loader = Mock(return_value=[1, 2, 3, 4])
        data_loader_kwargs = {"a": 1}
        model_updater = Mock(
            side_effect=[
                {"Model": "created"},
                {"Model": "updated"},
                {"Model": "not_changed"},
                {"Model": "updated"},
            ]
        )
        model_updater_kwargs = {"b": 2}

        updater = Updater(
            data_loader=data_loader,
            model_updater=model_updater,
            data_loader_kwargs=data_loader_kwargs,
            model_updater_kwargs=model_updater_kwargs,
        )
        results = updater.update()
        self.assertEqual(
            model_updater.mock_calls,
            [
                call(data=1, b=2),
                call(data=2, b=2),
                call(data=3, b=2),
                call(data=4, b=2),
            ],
        )
        self.assertEqual(
            results, {"Model": {"created": 1, "updated": 2, "not_changed": 1}}
        )

    def test_update_calculates_results__multiple_models(self):
        data_loader = Mock(return_value=[1, 2, 3, 4])
        data_loader_kwargs = {"a": 1}
        model_updater = Mock(
            side_effect=[
                {"Model1": "created", "Model2": "created"},
                {"Model1": "updated", "Model2": "updated"},
                {"Model1": "not_changed", "Model2": "created"},
                {"Model1": "updated", "Model2": "updated"},
            ]
        )
        model_updater_kwargs = {"b": 2}

        updater = Updater(
            data_loader=data_loader,
            model_updater=model_updater,
            data_loader_kwargs=data_loader_kwargs,
            model_updater_kwargs=model_updater_kwargs,
        )
        results = updater.update()
        self.assertEqual(
            results,
            {
                "Model1": {"created": 1, "updated": 2, "not_changed": 1},
                "Model2": {"created": 2, "updated": 2},
            },
        )

    def test_update__update_reference_model(self):
        """Tests that update create and update models"""
        ClinicFactory(external_id=1, abbreviation="C1")
        api_data = [
            {
                "id": 42,
                "external_id": 1,
                "abbreviation": "CL1",
                "description": "Clinic 1",
            },
            {
                "id": 42,
                "external_id": 2,
                "abbreviation": "CL2",
                "description": "Clinic 2",
            },
        ]
        data_loader = Mock(return_value=api_data)
        updater = Updater(
            data_loader=data_loader,
            model_updater=simple_model_updater,
            data_loader_kwargs={},
            model_updater_kwargs={
                "model": "references.Clinic",
                "identifiers": ["external_id"],
            },
            transformers=[delete_id],
        )
        updater.update()

        self.assertEqual(Clinic.objects.count(), 2)

        clinic_1 = Clinic.objects.get(external_id=1)
        clinic_2 = Clinic.objects.get(external_id=2)
        self.assertEqual(clinic_1.abbreviation, "CL1")
        self.assertEqual(clinic_2.abbreviation, "CL2")


class UpdaterFactoryTest(TestCase):
    @override_settings(
        UPDATE_SOURCES={
            "Clinic": {
                "data_loader": "updates.common.loaders.references_loader",
                "data_loader_kwargs": {"url": "/clinics/"},
                "transformers": [
                    "updates.common.transformers.delete_id",
                ],
                "model_updater": "updates.common.updaters.simple_model_updater",
                "model_updater_kwargs": {
                    "model": "references.Clinic",
                    "identifiers": ["external_id"],
                },
            },
        }
    )
    def test_create_updater(self):
        current_update = Mock()
        latest_update = Mock()
        updater = UpdaterFactory.create("Clinic", k1=1, k2=2)
        self.assertEqual(updater.data_loader, references_loader)
        self.assertEqual(
            updater.data_loader_kwargs, {"url": "/clinics/", "k1": 1, "k2": 2}
        )
        self.assertEqual(updater.model_updater, simple_model_updater)
        self.assertEqual(
            updater.model_updater_kwargs,
            {
                "model": "references.Clinic",
                "identifiers": ["external_id"],
                "k1": 1,
                "k2": 2,
            },
        )
        self.assertEqual(updater.transformers, [delete_id])

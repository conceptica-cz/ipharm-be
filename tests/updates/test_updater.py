from unittest import TestCase
from unittest.mock import Mock

from django.test import TestCase as DjangoTestCase
from django.test import override_settings
from references.models import Clinic
from updates.common.loaders import references_loader
from updates.common.transformers import delete_id
from updates.common.updaters import simple_model_updater
from updates.updater import Updater, UpdaterFactory

from factories.references.clinics import ClinicFactory
from factories.updates.updates import UpdateFactory


class UpdaterTest(DjangoTestCase):
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
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
        update = UpdateFactory()
        updater = Updater(
            update_model=update,
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
                "data_loader_kwargs": {"url": "/clinics/", "token": "token"},
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
        update = UpdateFactory()
        updater = UpdaterFactory.create(
            source="Clinic", k1=1, k2=2, update_model=update
        )
        self.assertEqual(updater.data_loader, references_loader)
        self.assertEqual(
            updater.data_loader_kwargs,
            {
                "url": "/clinics/",
                "k1": 1,
                "k2": 2,
                "update_id": update.id,
                "token": "token",
            },
        )
        self.assertEqual(updater.model_updater, simple_model_updater)
        self.assertEqual(
            updater.model_updater_kwargs,
            {
                "model": "references.Clinic",
                "identifiers": ["external_id"],
                "k1": 1,
                "k2": 2,
                "update_id": update.id,
            },
        )
        self.assertEqual(updater.transformers, [delete_id])

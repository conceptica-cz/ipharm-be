from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from updates.models import ModelUpdate
from updates.services import finish_update

from factories.updates.updates import UpdateFactory


class TestFinishUpdate(TestCase):
    def setUp(self) -> None:
        self.update = UpdateFactory()
        self.update_results = [
            {"Model1": "created", "Model2": "created"},
            {"Model1": "updated", "Model2": "updated"},
            {"Model1": "not_changed", "Model2": "created"},
            {"Model1": "updated", "Model2": "updated"},
        ]

    @patch("updates.services.timezone.now")
    def test_finish_update__finishes_update(self, mocked_now):
        now = timezone.datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        mocked_now.return_value = now
        finish_update(update_results=self.update_results, update_id=self.update.pk)

        self.update.refresh_from_db()

        self.assertEqual(self.update.finished_at, now)

    @patch("updates.services.timezone.now")
    def test_finish_update__creates_model_update(self, mocked_now):
        now = timezone.datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        mocked_now.return_value = now
        finish_update(update_results=self.update_results, update_id=self.update.pk)

        self.assertEqual(ModelUpdate.objects.count(), 2)

        model1_update = ModelUpdate.objects.get(name="Model1")
        self.assertEqual(model1_update.update, self.update)
        self.assertEqual(model1_update.created, 1)
        self.assertEqual(model1_update.updated, 2)
        self.assertEqual(model1_update.not_changed, 1)

        model2_update = ModelUpdate.objects.get(name="Model2")
        self.assertEqual(model2_update.update, self.update)
        self.assertEqual(model2_update.created, 2)
        self.assertEqual(model2_update.updated, 2)
        self.assertEqual(model2_update.not_changed, 0)

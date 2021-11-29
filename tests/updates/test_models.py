from unittest.mock import Mock, call, patch

from django.test import TestCase
from django.utils import timezone
from updates.models import ModelUpdate, Source, Update

from factories.updates.updates import SourceFactory, UpdateFactory


class SourceManagerTest(TestCase):
    def test_get_or_create_from_settings__create(self):
        """Test that method create new instance"""
        reference = Source.objects.get_or_create_from_settings(name="Clinic")

        self.assertEqual(reference.name, "Clinic")

    def test_get_or_create_from_settings__update(self):
        """Test that method update existing instance"""
        SourceFactory()

        count = Source.objects.count()
        name = Source.objects.first().name
        source = Source.objects.get_or_create_from_settings(name=name)

        self.assertEqual(Source.objects.count(), count)
        self.assertEqual(source.name, name)


class UpdateTest(TestCase):
    @patch("updates.models.timezone.now")
    def test_finish_update(self, mocked_now):
        now = timezone.datetime(2020, 1, 1, 0, 0, 0)
        mocked_now.return_value = now
        update = UpdateFactory()
        update.finish_update(
            {
                "Model1": {"not_changed": 40},
                "Model2": {"created": 20, "updated": 10},
            }
        )
        self.assertEqual(update.finished_at, now)

        self.assertEquals(ModelUpdate.objects.count(), 2)

        model1 = ModelUpdate.objects.get(name="Model1")
        self.assertEqual(model1.created, 0)
        self.assertEqual(model1.updated, 0)
        self.assertEqual(model1.not_changed, 40)

        model2 = ModelUpdate.objects.get(name="Model2")
        self.assertEqual(model2.created, 20)
        self.assertEqual(model2.updated, 10)
        self.assertEqual(model2.not_changed, 0)


class SourceTest(TestCase):
    @patch("updates.models.UpdaterFactory.create")
    @patch("updates.models.timezone.now")
    def test_update(self, mocked_now, mocked_create):
        updater = Mock(
            update=Mock(
                return_value={
                    "Model1": {"not_changed": 40},
                    "Model2": {"created": 20, "updated": 10},
                }
            )
        )
        mocked_create.return_value = updater
        now = timezone.datetime(2021, 1, 1, 0, 0, 0)
        mocked_now.return_value = now

        source = SourceFactory()
        update_2 = UpdateFactory(
            source=source, started_at=timezone.datetime(2020, 1, 1, 2, 0, 0)
        )
        update_3 = UpdateFactory(
            source=source, started_at=timezone.datetime(2020, 1, 1, 3, 0, 0)
        )
        update_1 = UpdateFactory(
            source=source, started_at=timezone.datetime(2020, 1, 1, 1, 0, 0)
        )

        source.update()

        self.assertEqual(mocked_create.call_count, 1)
        self.assertEqual(Update.objects.count(), 4)
        self.assertEqual(ModelUpdate.objects.count(), 2)
        current_update = Update.objects.get(started_at=now)
        self.assertEqual(
            mocked_create.mock_calls[0],
            call(source.name, update=current_update, latest_update=update_3),
        )

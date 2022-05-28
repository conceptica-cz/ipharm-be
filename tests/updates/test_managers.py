from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone
from updates.models import ModelUpdate, Update

from factories.updates.updates import ModelUpdateFactory, UpdateFactory


class UpdateManagerTest(TestCase):
    @patch("updates.querysets.timezone.now")
    @override_settings(EMPTY_UPDATES_DELETING_TIME_GAP=1)
    def test_get_old_empty_update(self, mock_now):
        mock_now.return_value = timezone.datetime(2021, 10, 1, 10, tzinfo=timezone.utc)
        new_time = timezone.datetime(2021, 10, 1, 9, 2, tzinfo=timezone.utc)
        new_update = UpdateFactory(started_at=new_time)

        old_time = timezone.datetime(2021, 10, 1, 8, 58, tzinfo=timezone.utc)
        update_old_1 = UpdateFactory(started_at=old_time)
        ModelUpdateFactory(update=update_old_1)
        update_old_2 = UpdateFactory(started_at=old_time)
        update_old_3 = UpdateFactory(started_at=old_time)

        old_empty_updates = Update.objects.get_old_empty_updates()

        self.assertIn(update_old_2, old_empty_updates)
        self.assertIn(update_old_3, old_empty_updates)

        self.assertNotIn(update_old_1, old_empty_updates)
        self.assertNotIn(new_update, old_empty_updates)

    @patch("updates.querysets.timezone.now")
    @override_settings(EMPTY_UPDATES_DELETING_TIME_GAP=1)
    def test_delete_old_empty_update(self, mock_now):
        mock_now.return_value = timezone.datetime(2021, 10, 1, 10, tzinfo=timezone.utc)
        new_time = timezone.datetime(2021, 10, 1, 9, 2, tzinfo=timezone.utc)
        new_update = UpdateFactory(started_at=new_time)

        old_time = timezone.datetime(2021, 10, 1, 8, 58, tzinfo=timezone.utc)
        update_old_1 = UpdateFactory(started_at=old_time)
        ModelUpdateFactory(update=update_old_1)
        update_old_2 = UpdateFactory(started_at=old_time)
        update_old_3 = UpdateFactory(started_at=old_time)

        Update.objects.delete_old_empty_updates()

        updates = Update.all_objects.all()

        self.assertNotIn(update_old_2, updates)
        self.assertNotIn(update_old_3, updates)

        self.assertIn(update_old_1, updates)
        self.assertIn(new_update, updates)


class ModelUpdateManagerTest(TestCase):
    @patch("updates.querysets.timezone.now")
    @override_settings(EMPTY_UPDATES_DELETING_TIME_GAP=1)
    def test_get_old_empty_update(self, mock_now):

        mock_now.return_value = timezone.datetime(
            2021, 10, 1, 9, 2, tzinfo=timezone.utc
        )
        new_model_update = ModelUpdateFactory(created=0, updated=0, not_changed=10)

        mock_now.return_value = timezone.datetime(
            2021, 10, 1, 8, 58, tzinfo=timezone.utc
        )
        model_update_old_1 = ModelUpdateFactory(created=1, updated=0, not_changed=10)
        model_update_old_2 = ModelUpdateFactory(created=0, updated=1, not_changed=10)
        model_update_old_3 = ModelUpdateFactory(created=0, updated=0, not_changed=10)
        model_update_old_4 = ModelUpdateFactory(created=0, updated=0, not_changed=10)

        mock_now.return_value = timezone.datetime(2021, 10, 1, 10, tzinfo=timezone.utc)

        old_empty_model_updates = ModelUpdate.objects.get_old_empty_updates()

        self.assertIn(model_update_old_3, old_empty_model_updates)
        self.assertIn(model_update_old_4, old_empty_model_updates)

        self.assertNotIn(model_update_old_1, old_empty_model_updates)
        self.assertNotIn(model_update_old_2, old_empty_model_updates)
        self.assertNotIn(new_model_update, old_empty_model_updates)

    @patch("updates.querysets.timezone.now")
    @override_settings(EMPTY_UPDATES_DELETING_TIME_GAP=1)
    def test_delete_old_empty_update(self, mock_now):

        mock_now.return_value = timezone.datetime(
            2021, 10, 1, 9, 2, tzinfo=timezone.utc
        )
        new_model_update = ModelUpdateFactory(created=0, updated=0, not_changed=10)

        mock_now.return_value = timezone.datetime(
            2021, 10, 1, 8, 58, tzinfo=timezone.utc
        )
        model_update_old_1 = ModelUpdateFactory(created=1, updated=0, not_changed=10)
        model_update_old_2 = ModelUpdateFactory(created=0, updated=1, not_changed=10)
        model_update_old_3 = ModelUpdateFactory(created=0, updated=0, not_changed=10)
        model_update_old_4 = ModelUpdateFactory(created=0, updated=0, not_changed=10)

        mock_now.return_value = timezone.datetime(2021, 10, 1, 10, tzinfo=timezone.utc)

        ModelUpdate.objects.delete_old_empty_updates()
        model_updates = ModelUpdate.all_objects.all()

        self.assertNotIn(model_update_old_3, model_updates)
        self.assertNotIn(model_update_old_4, model_updates)

        self.assertIn(model_update_old_1, model_updates)
        self.assertIn(model_update_old_2, model_updates)
        self.assertIn(new_model_update, model_updates)

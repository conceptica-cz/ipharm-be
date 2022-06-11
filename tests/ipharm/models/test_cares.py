from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone

from factories.ipharm import CareFactory


class CareTestCase(TestCase):
    @patch("ipharm.models.cares.timezone.now")
    @override_settings(CARE_LOCK_TIME_GAP=2)
    def test_is_locked(self, mocked_now):
        mocked_now.return_value = timezone.datetime(2020, 1, 3, 1, tzinfo=timezone.utc)
        care = CareFactory(
            finished_at=timezone.datetime(2020, 1, 1, tzinfo=timezone.utc)
        )
        self.assertEqual(care.is_locked, True)

        care = CareFactory(
            finished_at=timezone.datetime(2020, 1, 2, tzinfo=timezone.utc)
        )
        self.assertEqual(care.is_locked, False)

from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from ipharm.models import Care
from updates.bulovka.post_operations import finish_cares

from factories.ipharm import CareFactory


class TestFinishCares(TestCase):
    @patch("updates.bulovka.post_operations.timezone.now")
    def test_finish_cares(self, mock_now):
        now = timezone.datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_now.return_value = now

        CareFactory(
            external_id=139,
            patient__birth_number="1111111112",
            is_active=True,
            finished_at=None,
            clinic__external_id=2,
            clinic__reference_id=2,
        )
        CareFactory(
            external_id=140,
            patient__birth_number="1111111111",
            is_active=True,
            finished_at=None,
            clinic__external_id=1,
            clinic__reference_id=1,
        )
        CareFactory(
            external_id=141,
            patient__birth_number="1234567891",
            is_active=True,
            finished_at=None,
            clinic__external_id=1,
            clinic__reference_id=1,
        )
        transformed_data = [
            {
                "patient": {
                    "external_id": 41,
                    "first_name": "John",
                    "last_name": "Doe",
                    "birth_number": "1234567890",
                    "birth_date": "1987-04-02",
                    "insurance_company": "111",
                    "insurance_number": "1234567890",
                    "height": 160.0,
                    "weight": 57.0,
                },
                "care": {
                    "external_id": 141,
                    "department": 16,
                    "started_at": "2021-05-18T20:23+00:00",
                    "finished_at": None,
                    "main_diagnosis": "K519",
                },
                "dekurz": {
                    "made_at": "2021-09-23T20:29:00+00:00",
                    "doctor": 92328,
                    "department": 120,
                },
            },
            {
                "patient": {
                    "external_id": 42,
                    "first_name": "John",
                    "last_name": "Smith",
                    "birth_number": "1234567891",
                    "birth_date": "1987-04-02",
                    "insurance_company": "111",
                    "insurance_number": "1234567891",
                    "height": 160.0,
                    "weight": 57.0,
                },
                "care": {
                    "external_id": 142,
                    "department": 16,
                    "started_at": "2021-05-18T20:23+00:00",
                    "finished_at": None,
                    "main_diagnosis": "K519",
                },
                "dekurz": {
                    "made_at": "2021-09-23T20:29:00+00:00",
                    "doctor": 92328,
                    "department": 120,
                },
            },
        ]
        kwargs = {"url_parameters": {"clinicId": 1}, "update": None}

        finish_cares(transformed_data, **kwargs)

        care_139 = Care.objects.get(external_id=139)
        care_140 = Care.objects.get(external_id=140)
        care_141 = Care.objects.get(external_id=141)

        self.assertEqual(care_139.finished_at, None)
        self.assertEqual(care_139.is_active, True)

        self.assertEqual(care_140.finished_at, now)
        self.assertEqual(care_140.is_active, False)

        self.assertEqual(care_141.finished_at, None)
        self.assertEqual(care_141.is_active, True)

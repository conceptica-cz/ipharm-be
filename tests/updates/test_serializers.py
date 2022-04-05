from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils import timezone
from updates.serializers import ModelChangeSerializer

from factories.ipharm import PatientFactory
from factories.users import UserFactory


class ModelChangeSerializerTest(TestCase):
    @patch("simple_history.models.timezone.now")
    def test_get_changes(self, mocked_now: Mock):
        initial_time = timezone.datetime(2020, 1, 1, 0, tzinfo=timezone.utc)
        mocked_now.return_value = initial_time
        patient = PatientFactory(first_name="John", last_name="Doe")
        user_1 = UserFactory()
        user_2 = UserFactory()

        change_time = timezone.datetime(2020, 1, 1, 2, tzinfo=timezone.utc)
        mocked_now.return_value = change_time

        patient.first_name = "Joe"
        patient.last_name = "Smith"
        patient.save()
        history_record = patient.history.first()
        history_record.history_user = user_2
        history_record.save()

        change = list(patient.get_changes())[0]

        serializer = ModelChangeSerializer(change)

        self.assertEqual(
            serializer.data,
            {
                "date": "2020-01-01T03:00:00+01:00",
                "entity_name": "Patient",
                "entity_id": patient.id,
                "user": {
                    "id": user_2.id,
                    "username": user_2.username,
                    "first_name": user_2.first_name,
                    "last_name": user_2.last_name,
                    "email": user_2.email,
                },
                "field_changes": [
                    {
                        "field": "first_name",
                        "old_value": "John",
                        "new_value": "Joe",
                    },
                    {
                        "field": "last_name",
                        "old_value": "Doe",
                        "new_value": "Smith",
                    },
                ],
            },
        )

from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils import timezone

from factories.ipharm import PatientFactory
from factories.users import UserFactory


class PatientTest(TestCase):
    @patch("simple_history.models.timezone.now")
    def test_get_changes(self, mocked_now: Mock):
        initial_time = timezone.datetime(2020, 1, 1, 0, tzinfo=timezone.utc)
        mocked_now.return_value = initial_time
        patient = PatientFactory(first_name="John", last_name="Doe")
        user_1 = UserFactory()
        user_2 = UserFactory()

        first_change_time = timezone.datetime(2020, 1, 1, 1, tzinfo=timezone.utc)
        mocked_now.return_value = first_change_time

        patient.first_name = "Jane"
        patient.save()
        history_record = patient.history.first()
        history_record.history_user = user_1
        history_record.save()

        second_change_time = timezone.datetime(2020, 1, 1, 2, tzinfo=timezone.utc)
        mocked_now.return_value = second_change_time

        patient.first_name = "Joe"
        patient.last_name = "Smith"
        patient.save()
        history_record = patient.history.first()
        history_record.history_user = user_2
        history_record.save()

        changes = list(patient.get_changes())

        self.assertEqual(len(changes), 2)
        user_2_change = changes[0]
        user_1_change = changes[1]
        self.assertEqual(user_2_change.date, second_change_time)
        self.assertEqual(len(user_2_change.field_changes), 2)
        self.assertEqual(user_2_change.field_changes[0].field, "first_name")
        self.assertEqual(user_2_change.field_changes[0].old, "Jane")
        self.assertEqual(user_2_change.field_changes[0].new, "Joe")
        self.assertEqual(user_2_change.field_changes[1].field, "last_name")
        self.assertEqual(user_2_change.field_changes[1].old, "Doe")
        self.assertEqual(user_2_change.field_changes[1].new, "Smith")
        self.assertEqual(user_2_change.user, user_2)

        self.assertEqual(len(user_1_change.field_changes), 1)
        self.assertEqual(user_1_change.date, first_change_time)
        self.assertEqual(user_1_change.field_changes[0].field, "first_name")
        self.assertEqual(user_1_change.field_changes[0].old, "John")
        self.assertEqual(user_1_change.field_changes[0].new, "Jane")
        self.assertEqual(user_2_change.user, user_2)

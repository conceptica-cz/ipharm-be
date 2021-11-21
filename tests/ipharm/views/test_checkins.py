from django.urls import reverse
from ipharm.models import CheckIn
from references.serializers.drugs import DrugSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import CareFactory, CheckInFactory
from factories.references import DrugFactory
from factories.users.models import UserFactory


class CreateCheckInTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory()

    def test_create_checkin(self):
        self.client.force_login(user=self.user)
        drug_1 = DrugFactory()
        drug_2 = DrugFactory()
        drug_3 = DrugFactory()
        drug_4 = DrugFactory()
        data = {
            "care": self.care.pk,
            "drugs": [drug_1.pk, drug_3.pk, drug_4.pk],
            "polypharmacy": True,
            "polypharmacy_note": "polypharmacy_note",
        }

        response = self.client.post(reverse("checkin_list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        check_in = CheckIn.objects.get(pk=response.data["id"])
        self.assertEqual(check_in.care, self.care)
        self.assertEqual(check_in.polypharmacy, True)
        self.assertEqual(check_in.polypharmacy_note, "polypharmacy_note")
        self.assertEqual(check_in.drugs.count(), 3)


class GetCheckInTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.check_in = CheckInFactory()

    def test_get_checking(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse("checkin_detail", kwargs={"pk": self.check_in.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.check_in.pk)
        self.assertEqual(response.data["care"], self.check_in.care.pk)
        self.assertEqual(response.data["polypharmacy"], self.check_in.polypharmacy)
        self.assertEqual(
            response.data["polypharmacy_note"], self.check_in.polypharmacy_note
        )
        self.assertEqual(
            response.data["drugs"],
            [DrugSerializer(instance=drug).data for drug in self.check_in.drugs.all()],
        )
        self.assertEqual(
            response.data["high_interaction_potential_drugs"],
            [
                DrugSerializer(instance=drug).data
                for drug in self.check_in.high_interaction_potential_drugs.all()
            ],
        )
        self.assertEqual(
            response.data["narrow_therapeutic_window_drugs"],
            [
                DrugSerializer(instance=drug).data
                for drug in self.check_in.narrow_therapeutic_window_drugs.all()
            ],
        )


class UpdateCheckInTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.check_in = CheckInFactory(polypharmacy=False)

    def test_patch_checking(self):
        self.client.force_login(user=self.user)
        data = {
            "polypharmacy": True,
            "polypharmacy_note": "polypharmacy_note",
        }

        response = self.client.patch(
            reverse("checkin_detail", kwargs={"pk": self.check_in.pk}), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_in = CheckIn.objects.get(pk=response.data["id"])
        self.assertEqual(check_in.polypharmacy, True)
        self.assertEqual(check_in.polypharmacy_note, "polypharmacy_note")

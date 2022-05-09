from django.urls import reverse
from ipharm.models.checkins import CheckIn
from references.serializers.drugs import DrugSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import CareFactory, CheckInDiagnosisFactory, CheckInFactory
from factories.references import DiagnosisFactory, DrugFactory
from factories.users.models import UserFactory


class CreateCheckInTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory(checkin=None)
        CheckIn.objects.all().delete()

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

        response = self.client.post(reverse("ipharm:checkin_list"), data=data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
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
            reverse("ipharm:checkin_detail", kwargs={"pk": self.check_in.pk})
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
            reverse("ipharm:checkin_detail", kwargs={"pk": self.check_in.pk}), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        check_in = CheckIn.objects.get(pk=response.data["id"])
        self.assertEqual(check_in.polypharmacy, True)
        self.assertEqual(check_in.polypharmacy_note, "polypharmacy_note")


class CheckInDiagnosisListViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.check_in_1 = CheckInFactory()
        self.check_in_2 = CheckInFactory()
        self.check_in_diagnosis_1 = CheckInDiagnosisFactory(check_in=self.check_in_1)
        self.check_in_diagnosis_2 = CheckInDiagnosisFactory(check_in=self.check_in_1)
        self.check_in_diagnosis_3 = CheckInDiagnosisFactory(check_in=self.check_in_2)

    def test_get(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("ipharm:checkin_diagnosis_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)
        self.assertEqual(
            response.data["results"][0]["id"], self.check_in_diagnosis_1.pk
        )
        self.assertEqual(
            response.data["results"][1]["id"], self.check_in_diagnosis_2.pk
        )
        self.assertEqual(
            response.data["results"][2]["id"], self.check_in_diagnosis_3.pk
        )

    def test_get_check_in_filter(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("ipharm:checkin_diagnosis_list")
            + "?check_in={}".format(self.check_in_1.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            response.data["results"][0]["id"], self.check_in_diagnosis_1.pk
        )
        self.assertEqual(
            response.data["results"][1]["id"], self.check_in_diagnosis_2.pk
        )

    def test_post(self):
        diagnosis = DiagnosisFactory()

        data = {
            "check_in": self.check_in_1.pk,
            "diagnosis": diagnosis.pk,
        }

        self.client.force_login(user=self.user)

        response = self.client.post(reverse("ipharm:checkin_diagnosis_list"), data=data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        self.assertEqual(response.data["check_in"], self.check_in_1.pk)
        self.assertEqual(response.data["diagnosis"], data["diagnosis"])
        self.client.force_login(user=self.user)

        data = {
            "check_in": self.check_in_1.pk,
            "diagnosis": DiagnosisFactory().pk,
        }

        response = self.client.post(reverse("ipharm:checkin_diagnosis_list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["check_in"], self.check_in_1.pk)
        self.assertEqual(response.data["diagnosis"], data["diagnosis"])


class CheckInDiagnosisDetailViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.check_in = CheckInFactory()

    def test_get(self):
        diagnosis = DiagnosisFactory()
        check_in_diagnosis = CheckInDiagnosisFactory(
            check_in=self.check_in, diagnosis=diagnosis
        )
        drug_1 = DrugFactory()
        drug_2 = DrugFactory()
        check_in_diagnosis.drugs.set([drug_1, drug_2])

        self.client.force_login(user=self.user)
        resposne = self.client.get(
            reverse(
                "ipharm:checkin_diagnosis_detail", kwargs={"pk": check_in_diagnosis.pk}
            )
        )
        self.assertEqual(resposne.status_code, status.HTTP_200_OK)
        self.assertEqual(resposne.data["id"], check_in_diagnosis.pk)
        self.assertEqual(resposne.data["check_in"], check_in_diagnosis.check_in.pk)
        self.assertEqual(resposne.data["drugs"], [drug_1.pk, drug_2.pk])
        self.assertEqual(resposne.data["diagnosis"], diagnosis.pk)

    def test_patch(self):
        diagnosis = DiagnosisFactory()
        check_in_diagnosis = CheckInDiagnosisFactory(
            check_in=self.check_in, diagnosis=diagnosis
        )
        drug_1 = DrugFactory()
        drug_2 = DrugFactory()
        check_in_diagnosis.drugs.set([drug_1, drug_2])

        new_drug = DrugFactory()
        new_diagnosis = DiagnosisFactory()

        self.client.force_login(user=self.user)
        data = {"drugs": [new_drug.pk], "diagnosis": new_diagnosis.pk}

        response = self.client.patch(
            reverse(
                "ipharm:checkin_diagnosis_detail", kwargs={"pk": check_in_diagnosis.pk}
            ),
            data=data,
        )

        check_in_diagnosis.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(check_in_diagnosis.diagnosis, new_diagnosis)
        self.assertQuerysetEqual(
            check_in_diagnosis.drugs.all(), [new_drug], transform=lambda x: x
        )
        self.assertEqual(check_in_diagnosis.drugs.count(), 1)

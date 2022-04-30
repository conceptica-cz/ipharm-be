from django.urls import reverse
from ipharm.models.patient_informations import PatientInformation
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import CareFactory, PatientInformationFactory
from factories.users.models import UserFactory


class CreatePatientInformationTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory(checkin=None)
        PatientInformation.objects.all().delete()

    def test_create_history(self):
        self.client.force_login(user=self.user)
        data = {
            "care": self.care.pk,
            "name": "name",
            "text": "text",
        }

        response = self.client.post(
            reverse("ipharm:patient_information_list"), data=data
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        patient_information = PatientInformation.objects.get(pk=response.data["id"])
        self.assertEqual(patient_information.name, "name")
        self.assertEqual(patient_information.text, "text")


class GetPatientInformationListTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.patient_information = PatientInformationFactory()
        self.care_1 = CareFactory()
        self.care_2 = CareFactory()
        PatientInformation.objects.all().delete()

        self.patient_information_1_1 = PatientInformationFactory(care=self.care_1)
        self.patient_information_1_2 = PatientInformationFactory(care=self.care_1)
        self.patient_information_2_1 = PatientInformationFactory(care=self.care_2)
        self.patient_information_2_2 = PatientInformationFactory(care=self.care_2)

    def test_get__care_filter(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse("ipharm:patient_information_list"), {"care": self.care_1.pk}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(len(response.data["results"]), 2)


class GetPatientInformationTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.patient_information = PatientInformationFactory()

    def test_get_checking(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse(
                "ipharm:patient_information_detail",
                kwargs={"pk": self.patient_information.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data["id"], self.patient_information.pk)
        self.assertEqual(response.data["care"], self.patient_information.care.pk)
        self.assertEqual(response.data["text"], self.patient_information.text)


class UpdatePatientInformationTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.patient_information = PatientInformationFactory(text="old text")

    def test_patch_checking(self):
        self.client.force_login(user=self.user)
        data = {
            "text": "new text",
        }

        response = self.client.patch(
            reverse(
                "ipharm:patient_information_detail",
                kwargs={"pk": self.patient_information.pk},
            ),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient_information = PatientInformation.objects.get(pk=response.data["id"])
        self.assertEqual(patient_information.text, "new text")

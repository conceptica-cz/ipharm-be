from django.urls import reverse
from ipharm.models.cares import Care
from ipharm.serializers.cares import CareNestedSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import CareFactory
from factories.references.diagnoses import DiagnosisFactory
from factories.users.models import UserFactory


class GetCareTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory()

    def test_get_single_care(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("care_detail", kwargs={"pk": self.care.pk}))
        serializer = CareNestedSerializer(self.care)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_care_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("care_detail", kwargs={"pk": self.care.pk + 1})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteCareTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory()

    def test_delete(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(
            reverse("care_detail", kwargs={"pk": self.care.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Care.objects.count(), 0)

    def test_delete_care_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("care_detail", kwargs={"pk": 42}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateCareTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory()

    def test_patch_single_patient(self):
        self.client.force_login(user=self.user)
        new_diagnosis_1 = DiagnosisFactory()
        new_diagnosis_2 = DiagnosisFactory()
        response = self.client.patch(
            reverse("care_detail", kwargs={"pk": self.care.pk}),
            data={"diagnoses": [new_diagnosis_1.pk, new_diagnosis_2.pk]},
        )

        self.care.refresh_from_db()

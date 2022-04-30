from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils import timezone
from references.models import Drug
from references.serializers.drugs import DrugSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.drugs import DrugFactory
from factories.users.models import UserFactory


class GetAllDrugsTest(APITestCase):
    def test_get_all_drugs(self):
        DrugFactory()
        DrugFactory()
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(reverse("references:drug_list"))
        drugs = Drug.objects.all()
        serializer = DrugSerializer(drugs, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSingleDrugTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.drug_1 = DrugFactory()
        self.drug_2 = DrugFactory()
        self.drug_3 = DrugFactory()

    def test_get_valid_single_drug(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:drug_detail", kwargs={"pk": self.drug_2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = DrugSerializer(self.drug_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_drug(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("references:drug_detail", kwargs={"pk": 42}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

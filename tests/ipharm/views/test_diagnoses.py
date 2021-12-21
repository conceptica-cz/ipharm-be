from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils import timezone
from references.models import Diagnosis
from references.serializers.diagnoses import DiagnosisSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.diagnoses import DiagnosisFactory
from factories.users.models import UserFactory


class GetAllDiagnosisTest(APITestCase):
    def test_get_all_diagnoses(self):
        DiagnosisFactory()
        DiagnosisFactory()
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(reverse("diagnosis_list"))
        diagnoses = Diagnosis.objects.all()
        serializer = DiagnosisSerializer(diagnoses, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSingleDiagnosisTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.diagnosis_1 = DiagnosisFactory()
        self.diagnosis_2 = DiagnosisFactory()
        self.diagnosis_3 = DiagnosisFactory()

    def test_get_valid_single_diagnosis(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("diagnosis_detail", kwargs={"pk": self.diagnosis_2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = DiagnosisSerializer(self.diagnosis_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_diagnosis(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("diagnosis_detail", kwargs={"pk": 42}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

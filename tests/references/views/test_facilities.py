from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils import timezone
from references.models import MedicalFacility
from references.serializers import MedicalFacilitySerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references import MedicalFacilityFactory
from factories.users.models import UserFactory


class GetAllMedicalFacilityTest(APITestCase):
    def test_get_all_facilities(self):
        MedicalFacilityFactory()
        MedicalFacilityFactory()
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(reverse("references:medical_facility_list"))
        facilities = MedicalFacility.objects.all()
        serializer = MedicalFacilitySerializer(facilities, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSingleMedicalFacilityTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.medical_facility_1 = MedicalFacilityFactory()
        self.medical_facility_2 = MedicalFacilityFactory()
        self.medical_facility_3 = MedicalFacilityFactory()

    def test_get_valid_single_medical_facility(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(
                "references:medical_facility_detail",
                kwargs={"pk": self.medical_facility_2.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = MedicalFacilitySerializer(self.medical_facility_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_medical_facility(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:medical_facility_detail", kwargs={"pk": 42})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

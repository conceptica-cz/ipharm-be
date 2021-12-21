from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils import timezone
from references.models import InsuranceCompany
from references.serializers.insurances import InsuranceCompanySerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.insurances import InsuranceCompanyFactory
from factories.users.models import UserFactory


class GetAllInsuranceCompanysTest(APITestCase):
    def test_get_all_insurances(self):
        InsuranceCompanyFactory()
        InsuranceCompanyFactory()
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(reverse("insurance_company_list"))
        insurances = InsuranceCompany.objects.all()
        serializer = InsuranceCompanySerializer(insurances, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSingleInsuranceCompanyTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.insurance_company_1 = InsuranceCompanyFactory()
        self.insurance_company_2 = InsuranceCompanyFactory()
        self.insurance_company_3 = InsuranceCompanyFactory()

    def test_get_valid_single_insurance_company(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(
                "insurance_company_detail", kwargs={"pk": self.insurance_company_2.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = InsuranceCompanySerializer(self.insurance_company_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_insurance_company(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("insurance_company_detail", kwargs={"pk": 42})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

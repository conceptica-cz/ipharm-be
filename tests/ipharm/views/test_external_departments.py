from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils import timezone
from references.models import ExternalDepartment
from references.serializers.external_departments import ExternalDepartmentSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.external_departments import ExternalDepartmentFactory
from factories.users.models import UserFactory


class GetAllExternalDepartmentsTest(APITestCase):
    def test_get_all_external_departments(self):
        ExternalDepartmentFactory()
        ExternalDepartmentFactory()
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(reverse("external_department_list"))
        external_departments = ExternalDepartment.objects.all()
        serializer = ExternalDepartmentSerializer(external_departments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSingleExternalDepartmentTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.external_department_1 = ExternalDepartmentFactory()
        self.external_department_2 = ExternalDepartmentFactory()
        self.external_department_3 = ExternalDepartmentFactory()

    def test_get_valid_single_external_department(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(
                "external_department_detail",
                kwargs={"pk": self.external_department_2.id},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = ExternalDepartmentSerializer(self.external_department_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_external_department(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("external_department_detail", kwargs={"pk": 42})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

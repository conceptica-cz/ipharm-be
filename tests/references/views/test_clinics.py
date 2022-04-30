from django.urls import reverse
from references.models import Clinic, Department
from references.serializers import ClinicSerializer, DepartmentSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references import ClinicFactory, DepartmentFactory
from factories.users.models import UserFactory


class GetAllClinicsTest(APITestCase):
    def setUp(self) -> None:
        self.hospital_1 = ClinicFactory(is_hospital=True, is_ambulance=False)
        self.hospital_2 = ClinicFactory(is_hospital=True, is_ambulance=False)
        self.ambulance_1 = ClinicFactory(is_hospital=False, is_ambulance=True)
        self.ambulance_2 = ClinicFactory(is_hospital=False, is_ambulance=True)
        self.both_1 = ClinicFactory(is_hospital=True, is_ambulance=True)
        self.both_2 = ClinicFactory(is_hospital=True, is_ambulance=True)

        self.user = UserFactory()
        self.user.hospitals.add(self.hospital_1, self.both_1)
        self.user.ambulances.add(self.ambulance_1, self.both_1, self.both_2)
        self.user.save()

    def test_get_all_clinics(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("references:clinic_list"))
        clinics = Clinic.objects.get_with_counters()
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_ambulances_only(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:clinic_list"), data={"clinic_filter": "ambulances"}
        )
        clinics = Clinic.objects.get_ambulances()
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_hospitals_only(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:clinic_list"), data={"clinic_filter": "hospitals"}
        )
        clinics = Clinic.objects.get_hospitals()
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_my_hospitals_only(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:clinic_list"), data={"clinic_filter": "my_hospitals"}
        )
        clinics = Clinic.objects.get_my_hospitals(self.user)
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_my_ambulances_only(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:clinic_list"), data={"clinic_filter": "my_ambulances"}
        )
        clinics = Clinic.objects.get_my_ambulances(self.user)
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSingleClinicsTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.clinic_3 = ClinicFactory()

    def test_get_valid_single_clinic(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:clinic_detail", kwargs={"pk": self.clinic_2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = ClinicSerializer(
            Clinic.objects.get_with_counters().get(pk=self.clinic_2.pk)
        )  # serializer use fields from annotated queryset
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_clinic(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:clinic_detail", kwargs={"pk": self.clinic_3.id + 1})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllDepartmentsTest(APITestCase):
    def test_get_all_departments(self):
        DepartmentFactory()
        DepartmentFactory()
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(reverse("references:department_list"))
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSingleDepartmentTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.department_1 = DepartmentFactory()
        self.department_2 = DepartmentFactory()
        self.department_3 = DepartmentFactory()

    def test_get_valid_single_department(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:department_detail", kwargs={"pk": self.department_2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = DepartmentSerializer(self.department_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_department(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(
                "references:department_detail", kwargs={"pk": self.department_3.pk + 1}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

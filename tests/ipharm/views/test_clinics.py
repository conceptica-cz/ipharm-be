from django.urls import reverse
from references.models import Clinic
from references.serializers.clinics import ClinicSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.clinics import ClinicFactory
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
        response = self.client.get(reverse("clinic_list"))
        clinics = Clinic.objects.all()
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_ambulances_only(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("clinic_list"), data={"clinic_filter": "ambulances"}
        )
        clinics = Clinic.objects.get_ambulances()
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_hospitals_only(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("clinic_list"), data={"clinic_filter": "hospitals"}
        )
        clinics = Clinic.objects.get_hospitals()
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_my_hospitals_only(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("clinic_list"), data={"clinic_filter": "my_hospitals"}
        )
        clinics = Clinic.objects.get_my_hospitals(self.user)
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_my_ambulances_only(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("clinic_list"), data={"clinic_filter": "my_ambulances"}
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
            reverse("clinic_detail", kwargs={"pk": self.clinic_2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = ClinicSerializer(self.clinic_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_clinic(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("clinic_detail", kwargs={"pk": 42}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

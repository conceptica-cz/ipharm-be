from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm.patients import ClinicFactory, PatientFactory
from factories.users.models import UserFactory
from ipharm.models import Clinic, Patient
from ipharm.serializers.patients import ClinicSerializer, PatientSerializer


class GetAllClinicsTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        clinic_1 = ClinicFactory()
        clinic_2 = ClinicFactory()
        clinic_3 = ClinicFactory()

    def test_get_all_clinics(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("clinic_list"))
        clinics = Clinic.objects.all()
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


class GetAllPatientsTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.patient_1 = PatientFactory(clinic=self.clinic_1)
        self.patient_2 = PatientFactory(clinic=self.clinic_2)
        self.patient_3 = PatientFactory(clinic=self.clinic_1)

    def test_get_all_patients(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("patient_list"))
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filtered_by_clinic(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("patient_list"), data={"clinic": self.clinic_1.pk}
        )
        patients = Patient.objects.filter(clinic=self.clinic_1)
        serializer = PatientSerializer(patients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

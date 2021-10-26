from django.urls import reverse
from ipharm.models import Patient
from ipharm.serializers.patients import PatientSerializer
from references.models import Clinic
from references.serializers.clinics import ClinicSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm.patients import PatientFactory
from factories.references.clinics import AmbulanceFactory, ClinicFactory
from factories.users.models import UserFactory


class GetAllClinicsTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.clinic_3 = ClinicFactory()
        self.ambulance_1 = AmbulanceFactory()
        self.ambulance_2 = AmbulanceFactory()

    def test_get_all_clinics(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("clinic_list"))
        clinics = Clinic.objects.all()
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_only_ambulances(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("clinic_list"), data={"clinic_type": "ambulance"}
        )
        clinics = Clinic.objects.filter(clinic_type=Clinic.AMBULANCE)
        serializer = ClinicSerializer(clinics, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_my_clinics_only(self):
        self.user.clinics.add(self.clinic_1, self.clinic_3, self.ambulance_2)
        self.user.save()
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("clinic_list"), data={"my_clinics_only": "true"}
        )
        clinics = Clinic.objects.filter(user=self.user)
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

from django.urls import reverse
from ipharm.models import Patient
from ipharm.serializers.patients import PatientNestedSerializer, PatientSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm.patients import PatientFactory
from factories.references.clinics import ClinicFactory
from factories.references.diagnoses import DiagnosisFactory
from factories.users.models import UserFactory


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


class GetSinglePatientTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.patient = PatientFactory()

    def test_get_single_patient(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("patient_detail", kwargs={"pk": self.patient.pk})
        )
        serializer = PatientNestedSerializer(self.patient)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_patient_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("patient_detail", kwargs={"pk": 42}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_single_patient(self):
        self.client.force_login(user=self.user)
        current_diagnosis = self.patient.diagnoses.first()
        new_diagnosis_1 = DiagnosisFactory()
        new_diagnosis_2 = DiagnosisFactory()
        response = self.client.patch(
            reverse("patient_detail", kwargs={"pk": self.patient.pk}),
            data={"diagnoses": [new_diagnosis_1.pk, new_diagnosis_2.pk]},
        )

        self.patient.refresh_from_db()
        self.assertEqual(
            response.data["diagnoses"],
            [current_diagnosis.pk, new_diagnosis_1.pk, new_diagnosis_2.pk],
        )

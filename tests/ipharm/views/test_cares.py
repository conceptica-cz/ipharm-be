from django.urls import reverse
from ipharm.models import Care
from ipharm.serializers.cares import CareNestedSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import CareFactory
from factories.ipharm.patients import PatientFactory
from factories.references.clinics import ClinicFactory
from factories.references.diagnoses import DiagnosisFactory
from factories.users.models import UserFactory


class CreatePatientCareTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.patient = PatientFactory()
        self.clinic = ClinicFactory()
        self.diagnosis_1 = DiagnosisFactory()
        self.diagnosis_2 = DiagnosisFactory()

    def test_create_hospital_care(self):
        self.client.force_login(user=self.user)
        data = {
            "clinic": self.clinic.pk,
        }
        response = self.client.post(
            reverse(
                "patient_current_hospital_care", kwargs={"patient_pk": self.patient.pk}
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        care = Care.objects.get(pk=response.data["id"])
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.current_hospital_care, care)

    def test_get_not_allowed(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(
                "patient_current_hospital_care", kwargs={"patient_pk": self.patient.pk}
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_ambulance_care(self):
        self.client.force_login(user=self.user)
        data = {
            "clinic": self.clinic.pk,
        }
        response = self.client.post(
            reverse(
                "patient_current_ambulance_care", kwargs={"patient_pk": self.patient.pk}
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        care = Care.objects.get(pk=response.data["id"])
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.current_ambulance_care, care)

    def test_creating_hospital_care__if_patient_already_has_care(self):
        """
        Test that not possible to create hospital care if patient already has hospital care
        """
        self.client.force_login(user=self.user)
        CareFactory(
            patient=self.patient, care_type=Care.HOSPITALIZATION, clinic=self.clinic
        )
        data = {
            "clinic": self.clinic.pk,
        }
        response = self.client.post(
            reverse(
                "patient_current_hospital_care", kwargs={"patient_pk": self.patient.pk}
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_creating_ambulance_care__if_patient_already_has_care(self):
        """
        Test that not possible to create ambulance care if patient already has ambulance care
        """
        self.client.force_login(user=self.user)
        CareFactory(patient=self.patient, care_type=Care.AMBULATION, clinic=self.clinic)
        data = {
            "clinic": self.clinic.pk,
        }
        response = self.client.post(
            reverse(
                "patient_current_ambulance_care", kwargs={"patient_pk": self.patient.pk}
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class GetCareTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory()

    def test_get_single_care(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("care_detail", kwargs={"pk": self.care.pk}))
        serializer = CareNestedSerializer(self.care)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_care_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("care_detail", kwargs={"pk": self.care.pk + 1})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteCareTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory()

    def test_delete(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(
            reverse("care_detail", kwargs={"pk": self.care.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Care.objects.count(), 0)

    def test_delete_care_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("care_detail", kwargs={"pk": 42}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateCareTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory()

    def test_patch_single_patient(self):
        self.client.force_login(user=self.user)
        new_diagnosis_1 = DiagnosisFactory()
        new_diagnosis_2 = DiagnosisFactory()
        response = self.client.patch(
            reverse("care_detail", kwargs={"pk": self.care.pk}),
            data={"diagnoses": [new_diagnosis_1.pk, new_diagnosis_2.pk]},
        )

        self.care.refresh_from_db()
        self.assertEqual(
            response.data["diagnoses"],
            [new_diagnosis_1.pk, new_diagnosis_2.pk],
        )

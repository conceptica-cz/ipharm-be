import factory
from django.urls import reverse
from ipharm.filters import PatientFilter
from ipharm.models import Care, Patient
from ipharm.serializers.patients import PatientNestedSerializer, PatientSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import CareFactory
from factories.ipharm.patients import PatientFactory
from factories.references import InsuranceCompanyFactory
from factories.references.clinics import ClinicFactory
from factories.references.diagnoses import DiagnosisFactory
from factories.users.models import UserFactory


class GetAllPatientsTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.patient_0 = PatientFactory()

        self.patient_1_hospital_1 = PatientFactory()
        CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_1_hospital_1,
            clinic=self.clinic_1,
        )

        self.patient_2_hospital_1 = PatientFactory()
        CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_2_hospital_1,
            clinic=self.clinic_1,
        )

        self.patient_3_hospital_2 = PatientFactory()
        CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_3_hospital_2,
            clinic=self.clinic_2,
        )

        self.patient_4_hospital_2_ambulance_2 = PatientFactory()
        CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_4_hospital_2_ambulance_2,
            clinic=self.clinic_2,
        )
        CareFactory(
            care_type=Care.AMBULATION,
            patient=self.patient_4_hospital_2_ambulance_2,
            clinic=self.clinic_2,
        )

        self.patient_5_ambulance_1 = PatientFactory()
        CareFactory(
            care_type=Care.AMBULATION,
            patient=self.patient_5_ambulance_1,
            clinic=self.clinic_1,
        )

        self.patient_6_ambulance_2 = PatientFactory()
        CareFactory(
            care_type=Care.AMBULATION,
            patient=self.patient_6_ambulance_2,
            clinic=self.clinic_2,
        )

    def test_get_all_patients(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("patient_list"))
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filtered_by_hospital(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("patient_list"), data={"hospital": self.clinic_1.pk}
        )
        patients = PatientFilter({"hospital": self.clinic_1.pk}).qs
        serializer = PatientSerializer(patients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class CreatePatientTest(APITestCase):
    def setUp(self) -> None:
        self.insurance_company = InsuranceCompanyFactory()
        self.user = UserFactory()

    def test_new_patient_ambulance(self):
        patient_data = factory.build(dict, FACTORY_CLASS=PatientFactory)
        patient_data["insurance_company"] = self.insurance_company.pk
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("patient_list"), data=patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


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
        new_insurance_company = InsuranceCompanyFactory()
        new_first_name = "John"
        response = self.client.patch(
            reverse("patient_detail", kwargs={"pk": self.patient.pk}),
            data={
                "insurance_company": new_insurance_company.pk,
                "first_name": new_first_name,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.insurance_company, new_insurance_company)
        self.assertEqual(self.patient.first_name, new_first_name)

from django.test import TestCase
from django.utils import timezone
from ipharm.models import Care, Dekurz, Patient
from references.models import InsuranceCompany
from updates.bulovka.updaters import patient_updater

from factories.ipharm import CareFactory, PatientFactory
from factories.references import ClinicFactory, InsuranceCompanyFactory


class PatientUpdaterTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            "patient": {
                "external_id": 1364419,
                "first_name": "Ivana",
                "last_name": "Testovací",
                "birth_number": "1234567890",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "1234567890",
                "height": 160.0,
                "weight": 57.0,
            },
            "care": {
                "external_id": 828116,
                "department": 16,
                "started_at": "2021-05-18T20:23+00:00",
                "finished_at": None,
                "main_diagnosis": "K519",
            },
            "dekurz": {
                "made_at": "2021-09-23T20:29:00+00:00",
                "doctor": 92328,
                "department": 20,
            },
        }
        self.kwargs = {"url_parameters": {"clinicId": 1}, "update": None}

    def test_new_patient(self):
        operations = patient_updater(data=self.data, **self.kwargs)

        self.assertEqual(Patient.objects.count(), 1)
        patient = Patient.objects.get(external_id=1364419)

        self.assertEqual(InsuranceCompany.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 1)
        care = Care.objects.get(external_id=828116)
        self.assertEqual(Dekurz.objects.count(), 1)
        dekurz = Dekurz.objects.get(doctor__person_number="92328")

        self.assertEqual(patient.first_name, "Ivana")
        self.assertEqual(patient.insurance_company.code, "111")

        self.assertEqual(care.main_diagnosis.code, "K519")
        self.assertEqual(care.department.external_id, 16)
        self.assertEqual(care.clinic.external_id, 1)

        self.assertEqual(dekurz.department.external_id, 20)

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.CREATED,
                "ipharm.Care": Care.objects.CREATED,
            },
        )
        self.assertEqual(patient.current_hospital_care, care)

    def test_new_patient__care_with_same_id_but_another_clinic_exists(self):
        existing_clinic = ClinicFactory(external_id=2)
        patient = PatientFactory(external_id=1)
        existing_care = CareFactory(
            external_id=828116,
            clinic=existing_clinic,
            patient=patient,
        )

        operations = patient_updater(data=self.data, **self.kwargs)

        self.assertEqual(Patient.objects.count(), 2)
        patient = Patient.objects.get(external_id=1364419)

        self.assertEqual(InsuranceCompany.objects.count(), 2)
        self.assertEqual(Care.objects.count(), 2)
        self.assertEqual(Care.objects.filter(external_id=828116).count(), 2)
        care = Care.objects.get(external_id=828116, clinic__external_id=1)
        dekurz = Dekurz.objects.get(doctor__person_number="92328")

        self.assertEqual(patient.first_name, "Ivana")
        self.assertEqual(patient.insurance_company.code, "111")

        self.assertEqual(care.main_diagnosis.code, "K519")
        self.assertEqual(care.department.external_id, 16)
        self.assertEqual(care.clinic.external_id, 1)

        self.assertEqual(dekurz.department.external_id, 20)

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.CREATED,
                "ipharm.Care": Care.objects.CREATED,
            },
        )
        self.assertEqual(patient.current_hospital_care, care)

    def test_existing_not_changed_patient_and_care(self):
        patient_updater(data=self.data, **self.kwargs)
        operations = patient_updater(data=self.data, **self.kwargs)

        self.assertEqual(Patient.objects.count(), 1)

        self.assertEqual(InsuranceCompany.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 1)
        self.assertEqual(Dekurz.objects.count(), 1)

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.NOT_CHANGED,
                "ipharm.Care": Care.objects.NOT_CHANGED,
            },
        )

    def test_patient_changed(self):
        patient_updater(data=self.data, **self.kwargs)
        self.data["patient"]["first_name"] = "John"
        self.data["patient"]["last_name"] = "Doe"
        operations = patient_updater(data=self.data, **self.kwargs)

        self.assertEqual(Patient.objects.count(), 1)
        patient = Patient.objects.get(external_id=1364419)

        self.assertEqual(InsuranceCompany.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 1)
        self.assertEqual(Dekurz.objects.count(), 1)

        self.assertEqual(patient.first_name, "John")

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.UPDATED,
                "ipharm.Care": Care.objects.NOT_CHANGED,
            },
        )

    def test_care_changed(self):
        patient_updater(data=self.data, **self.kwargs)
        self.data["care"]["finished_at"] = "2021-05-25T18:23+00:00"
        operations = patient_updater(data=self.data, **self.kwargs)

        self.assertEqual(Patient.objects.count(), 1)

        self.assertEqual(InsuranceCompany.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 1)
        care = Care.objects.get(external_id=828116)
        self.assertEqual(Dekurz.objects.count(), 1)

        self.assertEqual(
            care.finished_at,
            timezone.datetime(2021, 5, 25, 18, 23, tzinfo=timezone.utc),
        )

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.NOT_CHANGED,
                "ipharm.Care": Care.objects.UPDATED,
            },
        )

    def test_dekurz_changed(self):
        """Tests that new Dekurz is created when Dekurz is changed."""

        patient_updater(data=self.data, **self.kwargs)
        self.data["dekurz"]["made_at"] = "2021-09-25T20:29:00+00:00"
        operations = patient_updater(data=self.data, **self.kwargs)

        self.assertEqual(Patient.objects.count(), 1)

        self.assertEqual(InsuranceCompany.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 1)
        self.assertEqual(Dekurz.objects.count(), 2)
        dekurz = Dekurz.objects.latest("made_at")

        self.assertEqual(
            dekurz.made_at,
            timezone.datetime(2021, 9, 25, 20, 29, tzinfo=timezone.utc),
        )

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.NOT_CHANGED,
                "ipharm.Care": Care.objects.UPDATED,
            },
        )

    def test_care_external_id_changed(self):
        """Tests that new Care is created when care_exiter_id is changed."""
        patient_updater(data=self.data, **self.kwargs)
        self.data["care"]["external_id"] = 828117
        operations = patient_updater(data=self.data, **self.kwargs)

        self.assertEqual(Patient.objects.count(), 1)
        patient = Patient.objects.get(external_id=1364419)

        self.assertEqual(InsuranceCompany.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 2)
        care = Care.objects.get(external_id=828117)
        self.assertEqual(Dekurz.objects.count(), 2)

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.UPDATED,
                "ipharm.Care": Care.objects.CREATED,
            },
        )

        self.assertEqual(patient.current_hospital_care, care)

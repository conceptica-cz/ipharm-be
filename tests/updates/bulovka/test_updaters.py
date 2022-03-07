from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone
from ipharm.models.cares import Care, Dekurz
from ipharm.models.patients import Patient
from references.models import InsuranceCompany
from updates.bulovka.updaters import patient_updater

from factories.ipharm import (
    CareFactory,
    CheckInFactory,
    PatientFactory,
    PatientInformationFactory,
    PharmacologicalEvaluationFactory,
    PharmacologicalPlanFactory,
    RiskDrugHistoryFactory,
)
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
                "department": 120,
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

        self.assertEqual(dekurz.department.external_id, 120)

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.CREATED,
                "ipharm.Care": Care.objects.CREATED,
            },
        )
        self.assertEqual(patient.current_care, care)

    def test_new_patient__care_with_same_id_but_another_clinic_exists(self):
        existing_clinic = ClinicFactory(external_id=2)
        patient = PatientFactory(external_id=1)
        existing_care = CareFactory(
            external_id=828116,
            clinic=existing_clinic,
            patient=patient,
            department__external_id=16,
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

        self.assertEqual(dekurz.department.external_id, 120)

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.CREATED,
                "ipharm.Care": Care.objects.CREATED,
            },
        )
        self.assertEqual(patient.current_care, care)

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

    @patch("django.utils.timezone.now")
    def test_care_external_id_changed(self, mocked_now):
        """Tests that new Care is created when care_external_id is changed."""
        now = timezone.datetime(2022, 1, 1, tzinfo=timezone.utc)
        mocked_now.return_value = now
        patient_updater(data=self.data, **self.kwargs)
        self.data["care"]["external_id"] = 828117
        operations = patient_updater(data=self.data, **self.kwargs)

        self.assertEqual(Patient.objects.count(), 1)
        patient = Patient.objects.get(external_id=1364419)

        self.assertEqual(InsuranceCompany.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 2)
        old_care = Care.objects.get(external_id=828116)
        care = Care.objects.get(external_id=828117)
        self.assertEqual(Dekurz.objects.count(), 2)

        self.assertEqual(
            operations,
            {
                "ipharm.Patient": Patient.objects.UPDATED,
                "ipharm.Care": Care.objects.CREATED,
            },
        )

        self.assertEqual(patient.current_care, care)

        self.assertEqual(old_care.finished_at, now)
        self.assertEqual(old_care.is_active, False)
        self.assertEqual(care.is_active, True)

    @patch("django.utils.timezone.now")
    def test_that_latest_care_is_always_current(self, mocked_now):
        """
        Test that regardless of processing order the latest care
        is always set as current and active.
        """
        now = timezone.datetime(2022, 1, 1, tzinfo=timezone.utc)
        mocked_now.return_value = now

        old_care_data = {
            "patient": {
                "external_id": 42,
                "first_name": "John",
                "last_name": "Doe",
                "birth_number": "1234567890",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "1234567890",
                "height": 160.0,
                "weight": 57.0,
            },
            "care": {
                "external_id": 142,
                "department": 16,
                "started_at": "2021-05-18T20:23+00:00",
                "finished_at": None,
                "main_diagnosis": "K519",
            },
            "dekurz": {
                "made_at": "2021-09-23T20:29:00+00:00",
                "doctor": 92328,
                "department": 120,
            },
        }
        new_care_data = {
            "patient": {
                "external_id": 42,
                "first_name": "John",
                "last_name": "Doe",
                "birth_number": "1234567890",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "1234567890",
                "height": 160.0,
                "weight": 57.0,
            },
            "care": {
                "external_id": 143,
                "department": 16,
                "started_at": "2021-05-19T20:23+00:00",
                "finished_at": None,
                "main_diagnosis": "K519",
            },
            "dekurz": {
                "made_at": "2021-05-20T20:29:00+00:00",
                "doctor": 92328,
                "department": 121,
            },
        }

        old_care_kwargs = {"url_parameters": {"clinicId": 1}, "update": None}
        new_care_kwargs = {"url_parameters": {"clinicId": 2}, "update": None}

        # Old care first
        patient_updater(data=old_care_data, **old_care_kwargs)
        patient_updater(data=new_care_data, **new_care_kwargs)

        old_care = Care.objects.get(external_id=142)
        new_care = Care.objects.get(external_id=143)

        self.assertEqual(old_care.is_active, False)
        self.assertEqual(new_care.is_active, True)
        self.assertEqual(old_care.finished_at, now)
        self.assertEqual(new_care.finished_at, None)
        self.assertEqual(Patient.objects.get(external_id=42).current_care, new_care)

        # New care first
        patient_updater(data=new_care_data, **new_care_kwargs)
        patient_updater(data=old_care_data, **old_care_kwargs)

        old_care = Care.objects.get(external_id=142)
        new_care = Care.objects.get(external_id=143)

        self.assertEqual(old_care.is_active, False)
        self.assertEqual(new_care.is_active, True)
        self.assertEqual(old_care.finished_at, now)
        self.assertEqual(new_care.finished_at, None)
        self.assertEqual(Patient.objects.get(external_id=42).current_care, new_care)

    @override_settings(MIGRATE_RELATED_TIME_GAP=72)
    def test_that_related_models_is_migrated__if_gap_is_less(self):
        """
        Test that if the time gap between last care and new care is less than
        settings.MIGRATE_RELATED_TIME_GAP all related models are migrated.
        """

        old_care = CareFactory(
            external_id=142,
            started_at=timezone.datetime(2021, 1, 1, tzinfo=timezone.utc),
            finished_at=timezone.datetime(2022, 1, 1, tzinfo=timezone.utc),
            patient__birth_number="1234567890",
        )
        check_in = CheckInFactory(care=old_care)
        plan = PharmacologicalPlanFactory(care=old_care)
        rdh = RiskDrugHistoryFactory(care=old_care)
        patient_information_1 = PatientInformationFactory(care=old_care)
        patient_information_2 = PatientInformationFactory(care=old_care)
        patient_information_3 = PatientInformationFactory(care=old_care)
        pharmacological_evaluation_1 = PharmacologicalEvaluationFactory(care=old_care)
        pharmacological_evaluation_2 = PharmacologicalEvaluationFactory(care=old_care)
        pharmacological_evaluation_3 = PharmacologicalEvaluationFactory(care=old_care)

        new_care_data = {
            "patient": {
                "external_id": 42,
                "first_name": "John",
                "last_name": "Doe",
                "birth_number": "1234567890",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "1234567890",
                "height": 160.0,
                "weight": 57.0,
            },
            "care": {
                "external_id": 143,
                "department": 16,
                "started_at": "2022-01-01T23:59+00:00",
                "finished_at": None,
                "main_diagnosis": "K519",
            },
            "dekurz": {
                "made_at": "2022-01-01T23:59+00:00",
                "doctor": 92328,
                "department": 121,
            },
        }

        kwargs = {"url_parameters": {"clinicId": 2}, "update": None}

        patient_updater(data=new_care_data, **kwargs)

        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 2)

        new_care = Care.objects.get(external_id=143)

        check_in.refresh_from_db()
        self.assertEqual(check_in.care, new_care)
        plan.refresh_from_db()
        self.assertEqual(plan.care, new_care)
        rdh.refresh_from_db()
        self.assertEqual(rdh.care, new_care)
        patient_information_1.refresh_from_db()
        self.assertEqual(patient_information_1.care, new_care)
        patient_information_2.refresh_from_db()
        self.assertEqual(patient_information_2.care, new_care)
        patient_information_3.refresh_from_db()
        self.assertEqual(patient_information_3.care, new_care)
        pharmacological_evaluation_1.refresh_from_db()
        self.assertEqual(pharmacological_evaluation_1.care, new_care)
        pharmacological_evaluation_2.refresh_from_db()
        self.assertEqual(pharmacological_evaluation_2.care, new_care)
        pharmacological_evaluation_3.refresh_from_db()
        self.assertEqual(pharmacological_evaluation_3.care, new_care)

    @override_settings(MIGRATE_RELATED_TIME_GAP=72)
    def test_that_related_models_is_not_migrated__if_gap_is_more(self):
        """
        Test that if the time gap between last care and new care is more than
        settings.MIGRATE_RELATED_TIME_GAP all related models are not migrated.
        """
        old_care_time = timezone.datetime(2022, 1, 1, tzinfo=timezone.utc)

        old_care = CareFactory(
            external_id=142,
            started_at=old_care_time,
            finished_at=old_care_time,
            patient__birth_number="1234567890",
        )
        check_in = CheckInFactory(care=old_care)
        plan = PharmacologicalPlanFactory(care=old_care)
        rdh = RiskDrugHistoryFactory(care=old_care)
        patient_information_1 = PatientInformationFactory(care=old_care)
        patient_information_2 = PatientInformationFactory(care=old_care)
        patient_information_3 = PatientInformationFactory(care=old_care)
        pharmacological_evaluation_1 = PharmacologicalEvaluationFactory(care=old_care)
        pharmacological_evaluation_2 = PharmacologicalEvaluationFactory(care=old_care)
        pharmacological_evaluation_3 = PharmacologicalEvaluationFactory(care=old_care)

        new_care_data = {
            "patient": {
                "external_id": 42,
                "first_name": "John",
                "last_name": "Doe",
                "birth_number": "1234567890",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "1234567890",
                "height": 160.0,
                "weight": 57.0,
            },
            "care": {
                "external_id": 143,
                "department": 16,
                "started_at": "2022-01-02T00:01+00:00",
                "finished_at": None,
                "main_diagnosis": "K519",
            },
            "dekurz": {
                "made_at": "2022-01-02T00:01+00:00",
                "doctor": 92328,
                "department": 121,
            },
        }

        kwargs = {"url_parameters": {"clinicId": 2}, "update": None}

        patient_updater(data=new_care_data, **kwargs)

        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Care.objects.count(), 2)

        new_care = Care.objects.get(external_id=143)

        check_in.refresh_from_db()
        self.assertEqual(check_in.care, new_care)
        plan.refresh_from_db()
        self.assertEqual(plan.care, new_care)
        rdh.refresh_from_db()
        self.assertEqual(rdh.care, new_care)
        patient_information_1.refresh_from_db()
        self.assertEqual(patient_information_1.care, new_care)
        patient_information_2.refresh_from_db()
        self.assertEqual(patient_information_2.care, new_care)
        patient_information_3.refresh_from_db()
        self.assertEqual(patient_information_3.care, new_care)
        pharmacological_evaluation_1.refresh_from_db()
        self.assertEqual(pharmacological_evaluation_1.care, new_care)
        pharmacological_evaluation_2.refresh_from_db()
        self.assertEqual(pharmacological_evaluation_2.care, new_care)
        pharmacological_evaluation_3.refresh_from_db()
        self.assertEqual(pharmacological_evaluation_3.care, new_care)

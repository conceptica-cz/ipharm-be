import datetime
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone
from django.utils.datetime_safe import date
from ipharm.models.cares import Care
from ipharm.models.checkins import CheckIn
from ipharm.models.patients import Patient

from factories.ipharm import (
    CareFactory,
    CheckInFactory,
    PatientFactory,
    PharmacologicalEvaluationFactory,
    PharmacologicalPlanFactory,
    RiskDrugHistoryFactory,
)
from factories.references import ClinicFactory, TagFactory


class PatientFilterPrefetchedClinicTest(TestCase):
    def setUp(self) -> None:
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.patient_0 = PatientFactory()

        self.patient_1 = PatientFactory()
        self.patient_1_care_1 = CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_1,
            clinic=self.clinic_1,
        )

        self.patient_2 = PatientFactory()
        self.patient_2_care_1 = CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_2,
            clinic=self.clinic_1,
        )

        self.patient_3 = PatientFactory()
        self.patient_3_care_1 = CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_3,
            clinic=self.clinic_2,
        )
        self.patient_3_care_2 = CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_3,
            clinic=self.clinic_1,
        )
        self.patient_3_care_3 = CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_3,
            clinic=self.clinic_1,
        )

        self.patient_4 = PatientFactory()
        self.patient_4_care_1 = CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_4,
            clinic=self.clinic_2,
        )
        self.patient_4_care_2 = CareFactory(
            care_type=Care.AMBULATION,
            patient=self.patient_4,
            clinic=self.clinic_2,
        )

    def test_clinic(self):
        filter_data = {"clinic": self.clinic_1.id}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
                self.patient_2,
                self.patient_3,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertEqual(patient_3.cares.count(), 2)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_2,
                self.patient_3_care_3,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_care_type_and_clinic(self):
        filter_data = {"clinic": self.clinic_2.id, "care_type": "hospitalization"}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_3,
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertEqual(patient_3.cares.count(), 1)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_4 = patients.get(id=self.patient_4.id)
        self.assertEqual(patient_4.cares.count(), 1)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )


class PatientFilterPrefetchedTagTest(TestCase):
    def setUp(self) -> None:
        self.tag_1 = TagFactory()
        self.tag_2 = TagFactory()
        self.tag_3 = TagFactory()
        self.tag_4 = TagFactory()
        self.tag_5 = TagFactory()
        self.tag_6 = TagFactory()
        self.tag_7 = TagFactory()
        self.patient_1 = PatientFactory()
        self.patient_2 = PatientFactory()
        self.patient_3 = PatientFactory()
        self.patient_4 = PatientFactory()

        self.patient_1_care_1 = CareFactory(patient=self.patient_1)
        self.patient_1_care_2 = CareFactory(patient=self.patient_1)
        self.patient_2_care_1 = CareFactory(patient=self.patient_2)
        self.patient_2_care_2 = CareFactory(patient=self.patient_2)
        self.patient_3_care_1 = CareFactory(patient=self.patient_3)
        self.patient_4_care_1 = CareFactory(patient=self.patient_4)

        pharmacological_plan_1 = PharmacologicalPlanFactory(care=self.patient_1_care_1)
        pharmacological_plan_2 = PharmacologicalPlanFactory(care=self.patient_1_care_2)
        pharmacological_plan_3 = PharmacologicalPlanFactory(care=self.patient_2_care_1)
        pharmacological_plan_4 = PharmacologicalPlanFactory(care=self.patient_2_care_2)
        pharmacological_plan_5 = PharmacologicalPlanFactory(care=self.patient_3_care_1)
        pharmacological_plan_6 = PharmacologicalPlanFactory(care=self.patient_4_care_1)

        pharmacological_plan_1.tags.set([self.tag_1, self.tag_2, self.tag_7])
        pharmacological_plan_2.tags.set([self.tag_1, self.tag_7])

        patient_1_care_1_evaluation_1 = PharmacologicalEvaluationFactory(
            care=self.patient_1_care_1
        )
        patient_1_care_1_evaluation_2 = PharmacologicalEvaluationFactory(
            care=self.patient_1_care_1
        )
        patient_1_care_2_evaluation_1 = PharmacologicalEvaluationFactory(
            care=self.patient_1_care_2
        )
        patient_2_care_1_evaluation_1 = PharmacologicalEvaluationFactory(
            care=self.patient_2_care_1
        )
        patient_2_care_2_evaluation_1 = PharmacologicalEvaluationFactory(
            care=self.patient_2_care_2
        )
        patient_3_care_1_evaluation_1 = PharmacologicalEvaluationFactory(
            care=self.patient_3_care_1
        )

        patient_1_care_1_evaluation_1.tags.set([self.tag_3, self.tag_4, self.tag_7])
        patient_1_care_1_evaluation_2.tags.set([self.tag_3, self.tag_7])
        patient_1_care_2_evaluation_1.tags.set([self.tag_4, self.tag_7])
        patient_2_care_1_evaluation_1.tags.set([self.tag_7])

        patient_1_care_1_history_1 = RiskDrugHistoryFactory(care=self.patient_1_care_1)
        patient_1_care_2_history_1 = RiskDrugHistoryFactory(care=self.patient_1_care_2)
        RiskDrugHistoryFactory(care=self.patient_2_care_1)
        RiskDrugHistoryFactory(care=self.patient_2_care_2)
        RiskDrugHistoryFactory(care=self.patient_3_care_1)
        RiskDrugHistoryFactory(care=self.patient_4_care_1)

        patient_1_care_1_history_1.tags.set([self.tag_5, self.tag_6, self.tag_7])
        patient_1_care_2_history_1.tags.set([self.tag_5, self.tag_7])

    def test_pharmacological_plan_tags(self):
        filter_data = {"tag": self.tag_1.id}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
                self.patient_1_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"tag": self.tag_2.id}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_pharmacological_evaluation_tags(self):
        filter_data = {"tag": self.tag_3.id}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"tag": self.tag_4.id}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
                self.patient_1_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"tag": self.tag_7.id}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
                self.patient_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
                self.patient_1_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_2 = patients.get(id=self.patient_2.id)
        self.assertQuerysetEqual(
            patient_2.cares.all(),
            [
                self.patient_2_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_risk_drug_history_tags(self):
        filter_data = {"tag": self.tag_5.id}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
                self.patient_1_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"tag": self.tag_6.id}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )


class PatientFilterPrefetchedByAgeInTest(TestCase):
    def setUp(self) -> None:
        self.now = timezone.datetime(2020, 2, 1)
        self.patient_20 = PatientFactory(birth_date=date(2000, 1, 1))
        self.patient_19_1 = PatientFactory(birth_date=date(2001, 3, 1))
        self.patient_19_2 = PatientFactory(birth_date=date(2002, 1, 1))
        self.patient_18_1 = PatientFactory(birth_date=date(2003, 3, 1))
        self.patient_18_2 = PatientFactory(birth_date=date(2004, 1, 1))

    @patch("ipharm.querysets.patients.timezone.now")
    def test_age(self, mocked_now):
        mocked_now.return_value = self.now

        filter_data = {"age": 19}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_19_1,
                self.patient_19_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    @patch("ipharm.querysets.patients.timezone.now")
    def test_age_min(self, mocked_now):
        mocked_now.return_value = self.now

        filter_data = {"age_min": 19}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [self.patient_19_1, self.patient_19_2, self.patient_20],
            transform=lambda x: x,
            ordered=False,
        )

    @patch("ipharm.querysets.patients.timezone.now")
    def test_age_max(self, mocked_now):
        mocked_now.return_value = self.now

        filter_data = {"age_max": 19}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_19_1,
                self.patient_19_2,
                self.patient_18_1,
                self.patient_18_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )


class PatientFilterPrefetchedCheckInTest(TestCase):
    def setUp(self) -> None:
        self.patient_1 = PatientFactory(first_name="Patient", last_name="1")
        self.patient_1_care_1 = CareFactory(
            patient=self.patient_1,
            started_at=timezone.datetime(2020, 1, 1, tzinfo=timezone.utc),
            finished_at=None,
        )

        self.patient_2 = PatientFactory(first_name="Patient", last_name="2")
        self.patient_2_care_1 = CareFactory(
            patient=self.patient_2,
            started_at=timezone.datetime(2020, 2, 1, tzinfo=timezone.utc),
            finished_at=timezone.datetime(2020, 2, 2, tzinfo=timezone.utc),
        )
        self.patient_2_care_2 = CareFactory(
            patient=self.patient_2,
            started_at=timezone.datetime(2020, 2, 4, tzinfo=timezone.utc),
            finished_at=None,
        )
        CheckInFactory(
            care=self.patient_2_care_2,
            risk_level=1,
        )

        self.patient_3 = PatientFactory(first_name="Patient", last_name="3")
        self.patient_3_care_1 = CareFactory(
            patient=self.patient_3,
            started_at=timezone.datetime(2020, 1, 1, tzinfo=timezone.utc),
            finished_at=timezone.datetime(2020, 1, 2, tzinfo=timezone.utc),
        )
        CheckInFactory(
            care=self.patient_3_care_1,
            risk_level=1,
        )
        self.patient_3_care_2 = CareFactory(
            patient=self.patient_3,
            started_at=timezone.datetime(2020, 1, 4, tzinfo=timezone.utc),
            finished_at=None,
        )
        CheckInFactory(
            care=self.patient_3_care_2,
            risk_level=2,
        )

        self.patient_4 = PatientFactory(first_name="Patient", last_name="4")
        self.patient_4_care_1 = CareFactory(
            patient=self.patient_4,
            started_at=timezone.datetime(2020, 1, 1, tzinfo=timezone.utc),
            finished_at=timezone.datetime(2020, 1, 2, tzinfo=timezone.utc),
        )
        CheckInFactory(
            care=self.patient_4_care_1,
            risk_level=3,
        )
        self.patient_4_care_2 = CareFactory(
            patient=self.patient_4,
            started_at=timezone.datetime(2020, 1, 4, tzinfo=timezone.utc),
            finished_at=None,
        )
        CheckInFactory(
            care=self.patient_4_care_2,
            risk_level=1,
        )

    def test_has_checkin(self):
        filter_data = {"has_checkin": False}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
                self.patient_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_2 = patients.get(id=self.patient_2.id)
        self.assertQuerysetEqual(
            patient_2.cares.all(),
            [
                self.patient_2_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"has_checkin": True}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_2,
                self.patient_3,
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_2 = patients.get(id=self.patient_2.id)
        self.assertQuerysetEqual(
            patient_2.cares.all(),
            [
                self.patient_2_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_1,
                self.patient_3_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_4 = patients.get(id=self.patient_4.id)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_1,
                self.patient_4_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_risk_level(self):
        filter_data = {"risk_level": 1}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_2,
                self.patient_3,
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_2 = patients.get(id=self.patient_2.id)
        self.assertQuerysetEqual(
            patient_2.cares.all(),
            [
                self.patient_2_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_4 = patients.get(id=self.patient_4.id)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"risk_level": 2}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_3,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"risk_level": 3}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_4 = patients.get(id=self.patient_4.id)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    @patch("ipharm.querysets.patients.timezone.now")
    @override_settings(CARE_LOCK_TIME_GAP=5)
    def test_is_locked(self, mocked_now):
        mocked_now.return_value = timezone.datetime(2020, 2, 5, tzinfo=timezone.utc)
        filter_data = {"is_locked": True}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_3,
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )
        patient_3 = patients.get(id=self.patient_3.id)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )
        patient_4 = patients.get(id=self.patient_4.id)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"is_locked": False}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
                self.patient_2,
                self.patient_3,
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_2 = patients.get(id=self.patient_2.id)
        self.assertQuerysetEqual(
            patient_2.cares.all(),
            [
                self.patient_2_care_1,
                self.patient_2_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_4 = patients.get(id=self.patient_4.id)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_care_date_from(self):
        filter_data = {"care_date_from": datetime.date(2020, 2, 2)}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
                self.patient_2,
                self.patient_3,
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )
        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )
        patient_2 = patients.get(id=self.patient_2.id)
        self.assertQuerysetEqual(
            patient_2.cares.all(),
            [
                self.patient_2_care_1,
                self.patient_2_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_4 = patients.get(id=self.patient_4.id)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        filter_data = {"care_date_to": datetime.date(2020, 1, 3)}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_3,
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_4 = patients.get(id=self.patient_4.id)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )


class PatientFilterPrefetchedPharmacologicalPlanTest(TestCase):
    def setUp(self) -> None:

        self.patient_1 = PatientFactory()
        self.patient_1_care_1 = CareFactory(
            patient=self.patient_1,
            started_at=timezone.datetime(2020, 1, 1, tzinfo=timezone.utc),
            finished_at=timezone.datetime(2020, 1, 2, tzinfo=timezone.utc),
        )
        CheckInFactory(
            care=self.patient_1_care_1,
            risk_level=2,
        )
        PharmacologicalPlanFactory(
            care=self.patient_1_care_1, notification_datetime=None
        )
        self.patient_1_care_2 = CareFactory(
            patient=self.patient_1,
            started_at=timezone.datetime(2020, 1, 4, tzinfo=timezone.utc),
        )
        CheckInFactory(
            care=self.patient_1_care_2,
            risk_level=2,
        )

        self.patient_2 = PatientFactory()
        self.patient_2_care_1 = CareFactory(
            patient=self.patient_2,
        )
        CheckInFactory(
            care=self.patient_2_care_1,
            risk_level=2,
        )
        PharmacologicalPlanFactory(care=self.patient_2_care_1)

        self.patient_3 = PatientFactory()
        self.patient_3_care_1 = CareFactory(
            patient=self.patient_3,
            started_at=timezone.datetime(2020, 1, 1, tzinfo=timezone.utc),
            finished_at=timezone.datetime(2020, 1, 2, tzinfo=timezone.utc),
        )
        CheckInFactory(
            care=self.patient_3_care_1,
            risk_level=2,
        )
        PharmacologicalPlanFactory(
            care=self.patient_3_care_1, notification_datetime=None
        )
        self.patient_3_care_2 = CareFactory(
            patient=self.patient_3,
            started_at=timezone.datetime(2020, 1, 4, tzinfo=timezone.utc),
        )
        CheckInFactory(
            care=self.patient_3_care_2,
            risk_level=2,
        )
        PharmacologicalPlanFactory(
            care=self.patient_3_care_2,
        )

        self.patient_4 = PatientFactory()
        self.patient_4_care_1 = CareFactory(
            patient=self.patient_4,
            started_at=timezone.datetime(2020, 1, 1, tzinfo=timezone.utc),
            finished_at=timezone.datetime(2020, 1, 2, tzinfo=timezone.utc),
        )
        CheckInFactory(
            care=self.patient_4_care_1,
            risk_level=2,
        )

    def test_has_notification_datetime(self):
        filter_data = {"has_notification_datetime": True}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_2,
                self.patient_3,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_2 = patients.get(id=self.patient_2.id)
        self.assertQuerysetEqual(
            patient_2.cares.all(),
            [
                self.patient_2_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_3 = patients.get(id=self.patient_3.id)
        self.assertQuerysetEqual(
            patient_3.cares.all(),
            [
                self.patient_3_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_pharmacological_plan(self):
        filter_data = {"has_pharmacologicalplan": False}
        patients = Patient.objects.filter_prefetched(**filter_data)

        self.assertQuerysetEqual(
            patients,
            [
                self.patient_1,
                self.patient_4,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_1 = patients.get(id=self.patient_1.id)
        self.assertQuerysetEqual(
            patient_1.cares.all(),
            [
                self.patient_1_care_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        patient_4 = patients.get(id=self.patient_4.id)
        self.assertQuerysetEqual(
            patient_4.cares.all(),
            [
                self.patient_4_care_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

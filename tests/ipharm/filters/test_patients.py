from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from django.utils.datetime_safe import date
from ipharm.filters import PatientFilter
from ipharm.models.cares import Care

from factories.ipharm import (
    CareFactory,
    CheckInFactory,
    PatientFactory,
    PatientInformationFactory,
    PharmacologicalEvaluationFactory,
    PharmacologicalPlanFactory,
    RiskDrugHistoryFactory,
)
from factories.references import ClinicFactory, TagFactory


class PatientFilterByClinicTest(TestCase):
    def setUp(self) -> None:
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

    def test_clinic(self):
        """
        Test 'clinic' filter
        """
        f = PatientFilter(data={"clinic": self.clinic_1.id})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_1_hospital_1,
                self.patient_2_hospital_1,
                self.patient_5_ambulance_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_care_type_and_clinic(self):
        f = PatientFilter(
            data={"clinic": self.clinic_1.id, "care_type": "hospitalization"}
        )
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_1_hospital_1,
                self.patient_2_hospital_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )


class PatientFilterByCheckInTest(TestCase):
    def setUp(self) -> None:
        self.patient_without_checkin = PatientFactory()

        self.patient_with_risk_level_1 = PatientFactory()
        care = CareFactory(
            patient=self.patient_with_risk_level_1,
        )
        CheckInFactory(
            care=care,
            risk_level=1,
        )

        self.patient_with_risk_level_3 = PatientFactory()
        care = CareFactory(
            patient=self.patient_with_risk_level_3,
        )
        CheckInFactory(
            care=care,
            risk_level=3,
        )

        self.patient_without_notification_datetime = PatientFactory()
        care = CareFactory(
            patient=self.patient_without_notification_datetime,
        )
        CheckInFactory(
            care=care,
            risk_level=2,
        )
        PharmacologicalPlanFactory(care=care, notification_datetime=None)

        self.patient_with_notification_datetime = PatientFactory()
        care = CareFactory(
            patient=self.patient_with_notification_datetime,
        )
        CheckInFactory(
            care=care,
            risk_level=2,
        )
        PharmacologicalPlanFactory(care=care)

    def test_has_checkin_filter(self):
        f = PatientFilter(data={"has_checkin": True})
        queryset = f.qs
        self.assertEqual(queryset.count(), 4)
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_with_risk_level_1,
                self.patient_with_risk_level_3,
                self.patient_without_notification_datetime,
                self.patient_with_notification_datetime,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        f = PatientFilter(data={"has_checkin": False})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_without_checkin,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_risk_level_filter(self):
        f = PatientFilter(data={"risk_level": 1})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_with_risk_level_1,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        f = PatientFilter(data={"risk_level": 3})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_with_risk_level_3,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    def test_has_notification_datetime_filter(self):
        f = PatientFilter(data={"has_notification_datetime": True})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_with_notification_datetime,
            ],
            transform=lambda x: x,
            ordered=False,
        )


class PatientFilterByAgeInTest(TestCase):
    def setUp(self) -> None:
        self.now = timezone.datetime(2020, 2, 1)
        self.patient_20 = PatientFactory(birth_date=date(2000, 1, 1))
        self.patient_19_1 = PatientFactory(birth_date=date(2001, 3, 1))
        self.patient_19_2 = PatientFactory(birth_date=date(2002, 1, 1))
        self.patient_18_1 = PatientFactory(birth_date=date(2003, 3, 1))
        self.patient_18_2 = PatientFactory(birth_date=date(2004, 1, 1))

    @patch("ipharm.filters.patients.timezone.now")
    def test_age(self, mocked_now):
        mocked_now.return_value = self.now
        f = PatientFilter(data={"age": 19})
        queryset = f.qs
        self.assertEqual(queryset.count(), 2)
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_19_1,
                self.patient_19_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    @patch("ipharm.filters.patients.timezone.now")
    def test_age_min(self, mocked_now):
        mocked_now.return_value = self.now
        f = PatientFilter(data={"age_min": 19})
        queryset = f.qs
        self.assertEqual(queryset.count(), 3)
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_19_1,
                self.patient_19_2,
                self.patient_20,
            ],
            transform=lambda x: x,
            ordered=False,
        )

    @patch("ipharm.filters.patients.timezone.now")
    def test_age_max(self, mocked_now):
        mocked_now.return_value = self.now
        f = PatientFilter(data={"age_max": 19})
        queryset = f.qs
        self.assertEqual(queryset.count(), 4)
        self.assertQuerysetEqual(
            queryset,
            [
                self.patient_19_1,
                self.patient_19_2,
                self.patient_18_1,
                self.patient_18_2,
            ],
            transform=lambda x: x,
            ordered=False,
        )


class PatientFilterByTags(TestCase):
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
        self.patient_5 = PatientFactory()
        self.patient_6 = PatientFactory()

        care_1 = CareFactory(patient=self.patient_1)
        care_2 = CareFactory(patient=self.patient_2)
        care_3 = CareFactory(patient=self.patient_3)
        care_4 = CareFactory(patient=self.patient_4)
        care_5 = CareFactory(patient=self.patient_5)
        care_6 = CareFactory(patient=self.patient_6)

        pharmacological_plan_1 = PharmacologicalPlanFactory(care=care_1)
        pharmacological_plan_2 = PharmacologicalPlanFactory(care=care_2)
        pharmacological_plan_3 = PharmacologicalPlanFactory(care=care_3)
        pharmacological_plan_4 = PharmacologicalPlanFactory(care=care_4)
        pharmacological_plan_5 = PharmacologicalPlanFactory(care=care_5)
        pharmacological_plan_6 = PharmacologicalPlanFactory(care=care_6)

        pharmacological_plan_1.tags.set([self.tag_1, self.tag_2, self.tag_7])
        pharmacological_plan_2.tags.set([self.tag_1, self.tag_7])

        pharmacological_evaluation_1_1 = PharmacologicalEvaluationFactory(care=care_1)
        pharmacological_evaluation_1_2 = PharmacologicalEvaluationFactory(care=care_1)
        pharmacological_evaluation_2_1 = PharmacologicalEvaluationFactory(care=care_2)
        pharmacological_evaluation_3_1 = PharmacologicalEvaluationFactory(care=care_3)
        pharmacological_evaluation_4_1 = PharmacologicalEvaluationFactory(care=care_4)
        pharmacological_evaluation_5_1 = PharmacologicalEvaluationFactory(care=care_5)

        pharmacological_evaluation_1_1.tags.set([self.tag_3, self.tag_4, self.tag_7])
        pharmacological_evaluation_1_2.tags.set([self.tag_3, self.tag_7])
        pharmacological_evaluation_2_1.tags.set([self.tag_4, self.tag_7])
        pharmacological_evaluation_3_1.tags.set([self.tag_7])

        risk_drug_history_1 = RiskDrugHistoryFactory(care=care_1)
        risk_drug_history_2 = RiskDrugHistoryFactory(care=care_2)
        risk_drug_history_3 = RiskDrugHistoryFactory(care=care_3)
        risk_drug_history_4 = RiskDrugHistoryFactory(care=care_4)
        risk_drug_history_5 = RiskDrugHistoryFactory(care=care_5)
        risk_drug_history_6 = RiskDrugHistoryFactory(care=care_6)

        risk_drug_history_1.tags.set([self.tag_5, self.tag_6, self.tag_7])
        risk_drug_history_2.tags.set([self.tag_5, self.tag_7])

    def test_pharmacological_plan_tags(self):
        f = PatientFilter(data={"tag": self.tag_1.id})
        queryset = f.qs
        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.patient_1, queryset)
        self.assertIn(self.patient_2, queryset)

        f = PatientFilter(data={"tag": self.tag_2.id})
        queryset = f.qs
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.patient_1, queryset)

    def test_pharmacological_evaluation_tags(self):
        f = PatientFilter(data={"tag": self.tag_3.id})
        queryset = f.qs
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.patient_1, queryset)

        f = PatientFilter(data={"tag": self.tag_4.id})
        queryset = f.qs
        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.patient_1, queryset)
        self.assertIn(self.patient_2, queryset)

        f = PatientFilter(data={"tag": self.tag_7.id})
        queryset = f.qs
        self.assertEqual(queryset.count(), 3)
        self.assertIn(self.patient_1, queryset)
        self.assertIn(self.patient_2, queryset)
        self.assertIn(self.patient_3, queryset)

    def test_risk_drug_history_tags(self):
        f = PatientFilter(data={"tag": self.tag_5.id})
        queryset = f.qs
        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.patient_1, queryset)
        self.assertIn(self.patient_2, queryset)

        f = PatientFilter(data={"tag": self.tag_6.id})
        queryset = f.qs
        self.assertEqual(queryset.count(), 1)
        self.assertIn(self.patient_1, queryset)

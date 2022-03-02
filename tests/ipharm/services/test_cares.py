from django.test import TestCase
from ipharm.models.checkins import CheckIn
from ipharm.models.patient_informations import PatientInformation
from ipharm.models.pharmacological_evaluations import PharmacologicalEvaluation
from ipharm.models.pharmacological_plans import PharmacologicalPlan
from ipharm.models.risk_drug_histories import RiskDrugHistory
from ipharm.services import cares

from factories.ipharm import (
    CareFactory,
    CheckInFactory,
    PatientInformationFactory,
    PharmacologicalEvaluationFactory,
    PharmacologicalPlanFactory,
    RiskDrugHistoryFactory,
)


class MigrateRelatedTest(TestCase):
    def test_migrate_related_migrates_related_checkin(self):
        care = CareFactory()
        check_in = CheckInFactory(care=care)

        new_care = CareFactory()

        cares.migrate_related(source_care=care, target_care=new_care)

        check_in.refresh_from_db()

        self.assertEqual(CheckIn.objects.count(), 1)
        self.assertEqual(check_in.care, new_care)

    def test_migrate_related_migrates_related_pharmacological_plan(self):
        care = CareFactory()
        plan = PharmacologicalPlanFactory(care=care)

        new_care = CareFactory()

        cares.migrate_related(source_care=care, target_care=new_care)

        plan.refresh_from_db()

        self.assertEqual(PharmacologicalPlan.objects.count(), 1)
        self.assertEqual(plan.care, new_care)

    def test_migrate_related_migrates_risk_drug_history(self):
        care = CareFactory()
        rdh = RiskDrugHistoryFactory(care=care)

        new_care = CareFactory()

        cares.migrate_related(source_care=care, target_care=new_care)

        rdh.refresh_from_db()

        self.assertEqual(RiskDrugHistory.objects.count(), 1)
        self.assertEqual(rdh.care, new_care)

    def test_migrate_related_migrates_patient_informations(self):
        care = CareFactory()
        patient_information_1 = PatientInformationFactory(care=care)
        patient_information_2 = PatientInformationFactory(care=care)
        patient_information_3 = PatientInformationFactory(care=care)

        new_care = CareFactory()

        cares.migrate_related(source_care=care, target_care=new_care)

        patient_information_1.refresh_from_db()
        patient_information_2.refresh_from_db()
        patient_information_3.refresh_from_db()

        self.assertEqual(PatientInformation.objects.count(), 3)
        self.assertEqual(patient_information_1.care, new_care)
        self.assertEqual(patient_information_2.care, new_care)
        self.assertEqual(patient_information_3.care, new_care)

    def test_migrate_related_migrates_pharmacological_evaluations(self):
        care = CareFactory()
        pharmacological_evaluation_1 = PharmacologicalEvaluationFactory(care=care)
        pharmacological_evaluation_2 = PharmacologicalEvaluationFactory(care=care)
        pharmacological_evaluation_3 = PharmacologicalEvaluationFactory(care=care)

        new_care = CareFactory()

        cares.migrate_related(source_care=care, target_care=new_care)

        pharmacological_evaluation_1.refresh_from_db()
        pharmacological_evaluation_2.refresh_from_db()
        pharmacological_evaluation_3.refresh_from_db()

        self.assertEqual(PharmacologicalEvaluation.objects.count(), 3)
        self.assertEqual(pharmacological_evaluation_1.care, new_care)
        self.assertEqual(pharmacological_evaluation_2.care, new_care)
        self.assertEqual(pharmacological_evaluation_3.care, new_care)

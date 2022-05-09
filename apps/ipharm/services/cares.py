from typing import TYPE_CHECKING

from ipharm.models.checkins import CheckIn
from ipharm.models.patient_informations import PatientInformation
from ipharm.models.pharmacological_evaluations import PharmacologicalEvaluation
from ipharm.models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)
from ipharm.models.risk_drug_histories import RiskDrugHistory

if TYPE_CHECKING:
    from ipharm.models.cares import Care


def migrate_related(source_care: "Care", target_care: "Care"):
    """
    Migrate the source care's related objects to target care
    """
    _migrate_check_in(source_care, target_care)
    _migrate_pharmacological_plan(source_care, target_care)
    _migrate_risk_drug_history(source_care, target_care)
    _migrate_patient_informations(source_care, target_care)
    _migrate_pharmacological_evaluations(source_care, target_care)


def _migrate_check_in(source_care, target_care):
    try:
        check_in = CheckIn.objects.get(care=source_care)
    except CheckIn.DoesNotExist:
        pass
    else:
        check_in.care = target_care
        check_in.save()


def _migrate_pharmacological_plan(source_care, target_care):
    try:
        plan = PharmacologicalPlan.objects.get(care=source_care)
    except PharmacologicalPlan.DoesNotExist:
        pass
    else:
        plan.care = target_care
        plan.save()


def _migrate_risk_drug_history(source_care, target_care):
    try:
        risk_drug_history = RiskDrugHistory.objects.get(care=source_care)
    except RiskDrugHistory.DoesNotExist:
        pass
    else:
        risk_drug_history.care = target_care
        risk_drug_history.save()


def _migrate_patient_informations(source_care, target_care):
    PatientInformation.objects.filter(care=source_care).update(care=target_care)


def _migrate_pharmacological_evaluations(source_care, target_care):
    PharmacologicalEvaluation.objects.filter(care=source_care).update(care=target_care)


class CareProcedures:
    def __init__(self, care: "Care"):
        self.care = care
        self.procedure_05751_count = None
        self.procedure_05753_count = None
        self.procedure_05755_count = None

    def count(self):
        self.procedure_05751_count = CheckIn.objects.filter(
            care=self.care, medical_procedure__isnull=False
        ).count()
        self.procedure_05753_count = PharmacologicalPlan.objects.filter(
            care=self.care, medical_procedure__isnull=False
        ).count()
        self.procedure_05755_count = PharmacologicalPlanComment.objects.filter(
            pharmacological_plan__care=self.care, medical_procedure__isnull=False
        ).count()

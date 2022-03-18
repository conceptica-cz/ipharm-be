from django.utils import timezone
from ipharm.models.checkins import CheckIn
from ipharm.models.pharmacological_evaluations import PharmacologicalEvaluation
from references.models import Department, Identification
from reports.models import ReportVariable


def _medical_procedures(year):
    procedures = {
        "05751": CheckIn.objects.filter(
            medical_procedure__code="05751", updated_at__year=year
        ).count(),
    }
    return procedures


def _risk_levels(year):
    risk_levels = {
        "1": CheckIn.objects.filter(risk_level="1", updated_at__year=year).count(),
        "2": CheckIn.objects.filter(risk_level="2", updated_at__year=year).count(),
        "3": CheckIn.objects.filter(risk_level="3", updated_at__year=year).count(),
    }
    return risk_levels


def _header(year):
    identification = Identification.objects.get_identification_for_insurance_report()
    department = Department.objects.get_department_for_insurance_report()
    header = {
        "year": year,
        "name": identification.name,
        "address": identification.address,
        "zip": identification.zip,
        "city": identification.city,
        "ico": identification.ico,
        "pcz": identification.pcz,
        "department_name": department.description,
        "department_icp": department.icp,
        "department_workplace_code": department.workplace_code,
    }
    return header


def _signature():
    signature = {
        "date": timezone.now().strftime("%d.%m.%Y").replace(".0", "."),
    }
    return signature


def _variables(report_type):
    variables = ReportVariable.objects.as_dict(report_type=report_type)
    variables["clinic_sum"] = variables.get("surgical_clinics", 0) + variables.get(
        "internal_clinics", 0
    )
    return variables


def _interventions(year):
    interventions = {
        "deployment": PharmacologicalEvaluation.objects.filter(
            deployment=True, updated_at__year=year
        ).count(),
        "deployment_ft_approach": PharmacologicalEvaluation.objects.filter(
            deployment=True, deployment_ft_approach=True, updated_at__year=year
        ).count(),
        "discontinuation": PharmacologicalEvaluation.objects.filter(
            discontinuation=True, updated_at__year=year
        ).count(),
        "discontinuation_adverse_effect": PharmacologicalEvaluation.objects.filter(
            discontinuation=True,
            discontinuation_adverse_effect=True,
            updated_at__year=year,
        ).count(),
        "discontinuation_renal_insufficiency": PharmacologicalEvaluation.objects.filter(
            discontinuation=True,
            discontinuation_renal_insufficiency=True,
            updated_at__year=year,
        ).count(),
        "discontinuation_drug_interaction": PharmacologicalEvaluation.objects.filter(
            discontinuation=True,
            discontinuation_drug_interaction=True,
            updated_at__year=year,
        ).count(),
        "discontinuation_overdosage": PharmacologicalEvaluation.objects.filter(
            discontinuation=True, discontinuation_overdosage=True, updated_at__year=year
        ).count(),
        "discontinuation_medical_intervention": PharmacologicalEvaluation.objects.filter(
            discontinuation=True,
            discontinuation_medical_intervention=True,
            updated_at__year=year,
        ).count(),
        "dose_change": PharmacologicalEvaluation.objects.filter(
            dose_change=True, updated_at__year=year
        ).count(),
        "dose_change_adverse_effect_risk": PharmacologicalEvaluation.objects.filter(
            dose_change=True,
            dose_change_adverse_effect_risk=True,
            updated_at__year=year,
        ).count(),
        "dose_change_renal_insufficiency": PharmacologicalEvaluation.objects.filter(
            dose_change=True,
            dose_change_renal_insufficiency=True,
            updated_at__year=year,
        ).count(),
        "dose_change_drug_interaction": PharmacologicalEvaluation.objects.filter(
            dose_change=True, dose_change_drug_interaction=True, updated_at__year=year
        ).count(),
        "specific_consultation": PharmacologicalEvaluation.objects.filter(
            specific_consultation=True, updated_at__year=year
        ).count(),
    }
    return interventions


def _risk_factors(year):
    risk_factors = {
        "polypharmacy": CheckIn.objects.filter(
            polypharmacy=True, updated_at__year=year
        ).count(),
        "narrow_therapeutic_window": CheckIn.objects.filter(
            narrow_therapeutic_window=True, updated_at__year=year
        ).count(),
        "high_interaction_potential": CheckIn.objects.filter(
            high_interaction_potential=True, updated_at__year=year
        ).count(),
        "renal_insufficiency": CheckIn.objects.filter(
            renal_insufficiency=True, updated_at__year=year
        ).count(),
        "hepatic_insufficiency": CheckIn.objects.filter(
            hepatic_insufficiency=True, updated_at__year=year
        ).count(),
        "significant_biochemical_changes": CheckIn.objects.filter(
            significant_biochemical_changes=True, updated_at__year=year
        ).count(),
        "intensive_care": CheckIn.objects.filter(
            intensive_care=True, updated_at__year=year
        ).count(),
        "systemic_corticosteroids": CheckIn.objects.filter(
            systemic_corticosteroids=True, updated_at__year=year
        ).count(),
    }
    return risk_factors


def uzis_loader(**kwargs):
    year = kwargs["year"]
    report_type = kwargs.get("report_type")
    data = {
        "variables": _variables(report_type),
        "header": _header(year),
        "signature": _signature(),
        "medical_procedures": _medical_procedures(year),
        "risk_levels": _risk_levels(year),
        "interventions": _interventions(year),
        "risk_factors": _risk_factors(year),
    }
    return data

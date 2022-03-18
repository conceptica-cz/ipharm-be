from django.utils import timezone
from ipharm.models.checkins import CheckIn
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


def uzis_loader(**kwargs):
    year = kwargs["year"]
    report_type = kwargs.get("report_type")
    data = {
        "variables": _variables(report_type),
        "header": _header(year),
        "signature": _signature(),
        "medical_procedures": _medical_procedures(year),
        "risk_levels": _risk_levels(year),
    }
    return data

from django.utils import timezone
from ipharm.models.checkins import CheckIn
from references.models import Department, Identification
from reports.models import ReportVariable


def _count_check_in_medical_procedures(year):
    procedures = {
        "05751": CheckIn.objects.filter(
            medical_procedure__code="05751", updated_at__year=year
        ).count(),
    }
    return procedures


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
        "medical_procedures": _count_check_in_medical_procedures(year),
    }
    return data

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
        "department_name": department.description,
    }
    return header


def _signature():
    signature = {
        "name": "PharmDr. Jana Gregorová, Ph.D.",
        "phone": "604753142",
        "email": "jana.gregorova@bulovka.cz",
        "date": timezone.now().strftime("%d.%m.%Y").replace(".0", "."),
    }
    return signature


def uzis_loader(**kwargs):
    year = kwargs["year"]
    variables = ReportVariable.objects.as_dict()
    data = {
        "variables": variables,
    }
    data["medical_procedures"] = _count_check_in_medical_procedures(year)
    data["header"] = _header(year)
    data["signature"] = _signature()
    return data

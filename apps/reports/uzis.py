from ipharm.models.checkins import CheckIn
from reports.models import ReportVariable


def _count_check_in_medical_procedures(year):
    procedures = {
        "medical_procedure_05751": CheckIn.objects.filter(
            medical_procedure__code="05751", updated_at__year=year
        ).count(),
    }
    return procedures


def uzis_loader(**kwargs):
    year = kwargs["year"]
    variables = ReportVariable.objects.as_dict()
    data = {
        "year": year,
        "variables": variables,
    }
    data = data | _count_check_in_medical_procedures(year)
    return data

import logging
import shutil
from itertools import chain

from django.conf import settings
from django.db.models import Sum
from django.template.loader import render_to_string
from ipharm.models.checkins import CheckIn
from ipharm.models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)
from references.models import (
    Department,
    Identification,
    InsuranceCompany,
    MedicalProcedure,
)
from reports.models import InsuranceReport

logger = logging.getLogger(__name__)


class InsuranceReportError(Exception):
    pass


class PaddingError(Exception):
    pass


def add_padding(padding_table: dict, key: str, value: str) -> None:
    value = str(value)
    if len(value) > padding_table[key]["length"]:
        raise PaddingError(f"{key} is too long: {value}")
    if padding_table[key]["padding"] == "left":
        padded_value = (padding_table[key]["length"] - len(value)) * " " + value
    else:
        padded_value = value + (padding_table[key]["length"] - len(value)) * " "
    return padded_value


def get_document_data(
    obj: CheckIn,
    department_for_insurance: Department,
    medical_procedure: MedicalProcedure,
    document_total_number: int,
    document_number: int,
) -> dict:
    """

    :param obj: CheckIn to calculate dosage from
    :param department_for_insurance: Department, which data is used for dosage report
    :return:
    """
    heading_padding = {
        "TYP": {"padding": "right", "length": 1},
        "ECID": {"padding": "left", "length": 7},
        "ESTR": {"padding": "left", "length": 1},
        "EPOC": {"padding": "left", "length": 1},
        "EPOR": {"padding": "left", "length": 3},
        "ECPO": {"padding": "right", "length": 3},
        "ETPP": {"padding": "right", "length": 1},
        "EICO": {"padding": "right", "length": 8},
        "EVAR": {"padding": "right", "length": 6},
        "EODB": {"padding": "right", "length": 3},
        "EROD": {"padding": "right", "length": 10},
        "EZDG": {"padding": "right", "length": 5},
        "EKO": {"padding": "right", "length": 1},
        "EICZ": {"padding": "right", "length": 8},
        "ECDZ": {"padding": "left", "length": 7},
        "EDAT": {"padding": "right", "length": 8},
        "ECCEL": {"padding": "right", "length": 10},
        "ECBOD": {"padding": "left", "length": 7},
        "EODZ": {"padding": "right", "length": 3},
        "EVARZ": {"padding": "right", "length": 6},
        "DTYP": {"padding": "right", "length": 1},
    }
    result_padding = {
        "TYP": {"padding": "right", "length": 1},
        "VDAT": {"padding": "right", "length": 8},
        "VKOD": {"padding": "right", "length": 5},
        "VPOC": {"padding": "left", "length": 1},
        "DTYP": {"padding": "right", "length": 1},
    }

    heading = {}
    result = {}

    heading["TYP"] = "E"
    heading["ECID"] = str(document_total_number)
    heading["ESTR"] = "0"
    heading["EPOC"] = "0"
    heading["EPOR"] = str(document_number)
    heading["ECPO"] = str(obj.care.patient.insurance_company.code)
    heading["ETPP"] = "1"
    heading["EICO"] = department_for_insurance.icp
    heading["EVAR"] = department_for_insurance.ns
    heading["EODB"] = department_for_insurance.specialization_code
    heading["EROD"] = str(obj.care.patient.insurance_number)
    heading["EZDG"] = str(obj.care.main_diagnosis.code)
    heading["EKO"] = ""
    heading["EICZ"] = obj.care.actual_department.icp
    heading["ECDZ"] = ""
    heading["EDAT"] = obj.care.started_at.strftime("%d%m%Y")
    heading["ECCEL"] = ""
    heading["ECBOD"] = str(round(medical_procedure.scores))
    heading["EODZ"] = obj.care.actual_department.specialization_code
    heading["EVARZ"] = ""
    heading["DTYP"] = ""

    for k, v in heading.items():
        heading[k] = add_padding(heading_padding, k, v)

    result["TYP"] = "V"
    result["VDAT"] = obj.updated_at.strftime("%d%m%Y")
    result["VKOD"] = medical_procedure.code
    result["VPOC"] = "1"
    result["DTYP"] = " "

    for k, v in result.items():
        result[k] = add_padding(result_padding, k, v)

    return {
        "heading": heading,
        "result": result,
    }


def get_dosage_data(
    insurance_company: InsuranceCompany,
    identification: Identification,
    year: int,
    month: int,
    documents: list,
) -> dict:
    """
    Create dosage data for insurance report.

    :param insurance_company: InsuranceCompany for which data is created.
    :param identification: Identification, which data is used for dosage report.
    :return: dictionary with dosage data
    """
    year = str(year)
    month = str(month)
    if len(month) == 1:
        month_with_prefix = "0" + month
    else:
        month_with_prefix = month

    documents_count = str(len(documents))
    documents_scoring = str(
        round(sum([float(d["heading"]["ECBOD"]) for d in documents]))
    )

    padding = {
        "TYP": {"padding": "right", "length": 1},
        "CHAR": {"padding": "right", "length": 1},
        "DTYP": {"padding": "right", "length": 2},
        "DICO": {"padding": "right", "length": 8},
        "DPOB": {"padding": "right", "length": 4},
        "DROK": {"padding": "left", "length": 4},
        "DMES": {"padding": "left", "length": 2},
        "DCID": {"padding": "left", "length": 6},
        "DPOC": {"padding": "left", "length": 3},
        "DBODY": {"padding": "left", "length": 11},
        "DFIN": {"padding": "left", "length": 18},
        "DDPP": {"padding": "right", "length": 1},
        "DVDR1": {"padding": "right", "length": 13},
        "DVDR2": {"padding": "right", "length": 13},
    }

    dosage = {}

    dosage["TYP"] = "D"
    dosage["CHAR"] = "P"
    dosage["DTYP"] = "90"
    dosage["DICO"] = identification.identifier
    dosage["DPOB"] = identification.identifier[:4]
    dosage["DROK"] = year
    dosage["DMES"] = month_with_prefix
    dosage["DCID"] = month
    dosage["DPOC"] = documents_count
    dosage["DBODY"] = documents_scoring
    dosage["DFIN"] = "0.00"
    dosage["DDPP"] = insurance_company.type
    dosage["DVDR1"] = "06:6.2.42"
    dosage["DVDR2"] = ""

    for k, v in dosage.items():
        dosage[k] = add_padding(padding, k, v)

    return dosage


def get_insurance_report_data(
    insurance_company: InsuranceCompany,
    year: int,
    month: int,
    start_number: int,
    identification: Identification,
    department_for_insurance: Department,
):
    documents = []
    check_ins = CheckIn.objects.filter(
        care__patient__insurance_company=insurance_company,
        medical_procedure__isnull=False,
        updated_at__year=year,
        updated_at__month=month,
    )
    pharmacological_plans = PharmacologicalPlan.objects.filter(
        care__patient__insurance_company=insurance_company,
        medical_procedure__isnull=False,
        updated_at__year=year,
        updated_at__month=month,
    )
    pharmacological_plan_comments = PharmacologicalPlanComment.objects.filter(
        pharmacological_plan__care__patient__insurance_company=insurance_company,
        medical_procedure__isnull=False,
        updated_at__year=year,
        updated_at__month=month,
    )

    all_objects = chain(check_ins, pharmacological_plans, pharmacological_plan_comments)

    for document_number, obj in enumerate(all_objects):
        document_total_number = start_number + document_number
        documents.append(
            get_document_data(
                obj=obj,
                medical_procedure=obj.medical_procedure,
                department_for_insurance=department_for_insurance,
                document_number=document_number + 1,
                document_total_number=document_total_number,
            )
        )

    dosage = get_dosage_data(
        insurance_company=insurance_company,
        identification=identification,
        year=year,
        month=month,
        documents=documents,
    )
    return {"documents": documents, "dosage": dosage}


def generate_insurance_report(
    insurance_company: InsuranceCompany,
    year: int,
    month: int,
    start_number: int,
    identification: Identification,
    department_for_insurance: Department,
):
    data = get_insurance_report_data(
        insurance_company=insurance_company,
        year=year,
        month=month,
        start_number=start_number,
        identification=identification,
        department_for_insurance=department_for_insurance,
    )
    content = render_to_string("reports/insurance_report.txt", data)
    documents_number = len(data["documents"])
    if documents_number:
        insurance_report, created = InsuranceReport.objects.update_or_create(
            insurance_company=insurance_company,
            year=year,
            month=month,
            defaults={
                "documents_number": documents_number,
                "data": data,
                "content": content,
            },
        )
        insurance_report.save_file()


def get_start_number(year: int):
    document_count = InsuranceReport.objects.filter(year=year).aggregate(
        document_count=Sum("documents_number")
    )["document_count"]
    return document_count + 1 if document_count else 1


def generate_all_reports(year: int, month: int):
    if month > 1:
        previous_month = month - 1
        previous_year = year
    else:
        previous_month = 12
        previous_year = year - 1

    try:
        identification = (
            Identification.objects.get_identification_for_insurance_report()
        )
    except Identification.DoesNotExist as ex:
        raise InsuranceReportError(
            "Identification 'for_insurance' does not exist"
        ) from ex

    try:
        department_for_insurance = (
            Department.objects.get_department_for_insurance_report()
        )
    except Department.DoesNotExist as ex:
        raise InsuranceReportError("Department 'for_insurance' does not exist") from ex

    shutil.rmtree(
        settings.MEDIA_ROOT
        / settings.INSURANCE_REPORT_FOLDER
        / f"{previous_year}/{previous_month}",
        ignore_errors=True,
    )
    for insurance_company in InsuranceCompany.objects.all():
        start_number = get_start_number(previous_year)
        logger.info(
            "Generating company insurance reports for previous month",
            extra={
                "insurance_company": insurance_company.code,
                "year": previous_year,
                "month": previous_month,
                "start_number": start_number,
            },
        )
        generate_insurance_report(
            insurance_company=insurance_company,
            year=previous_year,
            month=previous_month,
            start_number=start_number,
            identification=identification,
            department_for_insurance=department_for_insurance,
        )

    shutil.rmtree(settings.MEDIA_ROOT / f"dosages/{year}/{month}", ignore_errors=True)

    for insurance_company in InsuranceCompany.objects.all():
        start_number = get_start_number(year)
        logger.info(
            "Generating company insurance reports for current month",
            extra={
                "insurance_company": insurance_company.code,
                "year": year,
                "month": month,
                "start_number": start_number,
            },
        )
        generate_insurance_report(
            insurance_company=insurance_company,
            year=year,
            month=month,
            start_number=start_number,
            identification=identification,
            department_for_insurance=department_for_insurance,
        )

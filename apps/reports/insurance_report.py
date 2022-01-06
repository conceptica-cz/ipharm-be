from django.conf import settings
from ipharm.models import CheckIn
from references.models import Department, Identification, MedicalProcedure


class PaddingError(Exception):
    pass


def add_padding(padding_table: dict, key: str, value: str) -> None:
    if len(value) > padding_table[key]:
        raise PaddingError(f"{key} is too long: {value}")
    padded_value = (padding_table[key] - len(value)) * " " + value
    return padded_value


def check_in_dosage(
    check_in: CheckIn,
    department_for_insurance: Department,
    medical_procedure: MedicalProcedure,
) -> dict:
    """

    :param check_in: CheckIn to calculate dosage from
    :param department_for_insurance: Department, which data is used for dosage report
    :return:
    """
    heading_padding = {
        "TYP": 1,
        "ECID": 7,
        "ESTR": 1,
        "EPOC": 1,
        "EPOR": 3,
        "ECPO": 3,
        "ETPP": 1,
        "EICO": 8,
        "EVAR": 6,
        "EODB": 3,
        "EROD": 10,
        "EZDG": 5,
        "EKO": 1,
        "EICZ": 8,
        "ECDZ": 7,
        "EDAT": 8,
        "ECCEL": 10,
        "ECBOD": 7,
        "EODZ": 3,
        "EVARZ": 6,
        "DTYP": 1,
    }
    result_padding = {
        "TYP": 1,
        "VDAT": 8,
        "VKOD": 5,
        "VPOC": 1,
        "DTYP": 1,
    }

    heading = {}
    result = {}

    heading["TYP"] = "E"
    heading["ECID"] = "*******"
    heading["ESTR"] = "0"
    heading["EPOC"] = "0"
    heading["EPOR"] = "***"
    heading["ECPO"] = str(check_in.care.patient.insurance_company.code)
    heading["ETPP"] = "1"
    heading["EICO"] = department_for_insurance.icp
    heading["EVAR"] = department_for_insurance.ns
    heading["EODB"] = department_for_insurance.specialization_code
    heading["EROD"] = str(check_in.care.patient.insurance_number)
    heading["EZDG"] = str(check_in.care.main_diagnosis.code)
    heading["EKO"] = ""
    heading["EICZ"] = check_in.care.department.icp
    heading["ECDZ"] = ""
    heading["EDAT"] = check_in.care.started_at.strftime("%d%m%Y")
    heading["ECCEL"] = ""
    heading["ECBOD"] = str(medical_procedure.scores)
    heading["EODZ"] = check_in.care.department.specialization_code
    heading["EVARZ"] = ""
    heading["DTYP"] = ""

    for k, v in heading.items():
        heading[k] = add_padding(heading_padding, k, v)

    result["TYP"] = "V"
    result["VDAT"] = ""
    result["VKOD"] = ""
    result["VPOC"] = ""
    result["DTYP"] = ""

    for k, v in result.items():
        result[k] = add_padding(result_padding, k, v)

    return {
        "heading": heading,
        "result": result,
    }

import logging

logger = logging.getLogger(__name__)


def patient_transformer(data: dict) -> dict:
    logger.debug(f"Transforming patient data {data}")
    transformed = {
        "patient": {
            "external_id": data["patientId"],
            "first_name": data["name"].split(" ", 1)[1],
            "last_name": data["name"].split(" ", 1)[0],
            "birth_number": data["birthNumber"],
            "birth_date": data["birthDate"],
            "insurance_company": data["insuranceCompany"],
            "insurance_number": data["insuranceNumber"]
            if data["insuranceNumber"]
            else data["birthNumber"],
            "height": data.get("height"),
            "weight": data.get("weight"),
        },
        "care": {
            "external_id": data.get("hospitalizationId"),
            "department": data["departmentIn"],
            "started_at": data["dateIn"],
            "finished_at": data.get("dateOut"),
            "main_diagnosis": data.get("diagnosis"),
        },
        "dekurz": None,
    }
    if data.get("dekurzTime"):
        transformed["dekurz"] = {
            "made_at": data["dekurzTime"],
            "doctor": data["dekurzWho"],
            "department": data["dekurzDepartment"],
        }
    return transformed

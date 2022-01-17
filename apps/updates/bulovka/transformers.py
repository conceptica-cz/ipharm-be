import logging
from typing import Optional

from django.utils import timezone

logger = logging.getLogger(__name__)


def make_aware(dt: str) -> Optional[str]:
    if dt is None:
        return None
    naive = timezone.datetime.fromisoformat(dt)
    aware = timezone.make_aware(naive)
    return aware.isoformat()


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
            "started_at": make_aware(data["dateIn"]),
            "finished_at": make_aware(data.get("dateOut")),
            "main_diagnosis": data.get("diagnosis"),
        },
        "dekurz": None,
    }
    if data.get("dekurzTime"):
        transformed["dekurz"] = {
            "made_at": make_aware(data["dekurzTime"]),
            "doctor": data["dekurzWho"] if data["dekurzWho"] else None,
            "department": data["dekurzDepartment"],
        }
    return transformed

import copy
import logging

from ipharm.models import Care, Dekurz, Patient
from references.models import Clinic, Department, Person

logger = logging.getLogger(__name__)


def patient_updater(data: dict, **kwargs) -> dict:
    logger.debug(f"Updating patient {data}")
    data = copy.deepcopy(data)
    operations = {}
    update = kwargs["update"]
    clinic_id = kwargs["url_parameters"]["clinicId"]

    # patient handling

    patient, patient_operation = Patient.objects.update_or_create_from_dict(
        data=data["patient"],
        identifiers=["birth_number"],
        relations={
            "insurance_company": {
                "field": "insurance_company",
                "key": "code",
                "delete_source_field": True,
            }
        },
        update=update,
    )
    operations["ipharm.Patient"] = patient_operation

    # care handling

    clinic, _ = Clinic.objects.get_or_create_temporary(external_id=clinic_id)
    department, _ = Department.objects.get_or_create(
        external_id=data["care"]["department"],
        defaults={
            "clinic": clinic,
            "clinic_external_id": clinic_id,
        },
    )

    data["care"]["patient_id"] = patient.id
    data["care"]["department_id"] = department.id
    del data["care"]["department"]
    data["care"]["care_type"] = Care.HOSPITALIZATION
    data["care"]["clinic"] = clinic
    care, care_operation = Care.objects.update_or_create_from_dict(
        data=data["care"],
        identifiers=["external_id"],
        relations={
            "main_diagnosis": {
                "field": "main_diagnosis",
                "key": "code",
                "delete_source_field": True,
            },
        },
        update=update,
    )
    operations["ipharm.Care"] = care_operation

    if data["dekurz"]:
        dekurz_docktor, _ = Person.objects.get_or_create_temporary(
            person_number=data["dekurz"]["doctor"]
        )
        dekurz_department, _ = Department.objects.get_or_create_temporary(
            clinic=clinic,
            clinic_external_id=clinic_id,
            external_id=data["dekurz"]["department"],
        )
        dekurz, _ = Dekurz.objects.get_or_create(
            care=care,
            made_at=data["dekurz"]["made_at"],
            doctor=dekurz_docktor,
            department=dekurz_department,
        )
        if care.last_dekurz != dekurz:
            care.set_last_dekurz(dekurz)
            if care_operation == Care.objects.NOT_CHANGED:
                operations["ipharm.Care"] = Care.objects.UPDATED

    if patient.current_hospital_care != care:
        patient.set_current_care(care)
        if patient_operation == Patient.objects.NOT_CHANGED:
            operations["ipharm.Patient"] = Patient.objects.UPDATED

    return operations

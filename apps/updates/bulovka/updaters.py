import copy
import logging

from ipharm.models.cares import Care, Dekurz
from ipharm.models.patients import Patient
from references.models import Clinic, Department, Person
from updates.models import Update

logger = logging.getLogger(__name__)


def patient_updater(data: dict, **kwargs) -> dict:
    logger.debug(f"Updating patient {data}")
    data = copy.deepcopy(data)
    operations = {}
    update_id = kwargs["update_id"]
    try:
        update = Update.objects.get(id=update_id)
    except Update.DoesNotExist:
        update = None
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
        },
    )

    data["care"]["patient_id"] = patient.id
    data["care"]["department_id"] = department.id
    del data["care"]["department"]
    data["care"]["care_type"] = Care.HOSPITALIZATION
    data["care"]["clinic"] = clinic
    care, care_operation = Care.objects.update_or_create_from_dict(
        data=data["care"],
        identifiers=["external_id", "clinic"],
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
        if data["dekurz"]["doctor"]:
            dekurz_docktor, _ = Person.objects.get_or_create_temporary(
                person_number=data["dekurz"]["doctor"]
            )
        else:
            dekurz_docktor = None
        dekurz_department, _ = Department.objects.get_or_create_temporary(
            clinic=clinic,
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

    if patient.current_care != care:
        care.refresh_from_db()  # prevent care.started_at to be string
        patient.set_current_care(care)
        if patient_operation == Patient.objects.NOT_CHANGED:
            operations["ipharm.Patient"] = Patient.objects.UPDATED

    return operations

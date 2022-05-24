import logging
from typing import Iterable, Tuple, Union

import requests
from django.conf import settings
from django.utils import timezone
from ipharm.models.patients import Patient
from references.models import Person
from requisitions.models import Requisition

logger = logging.getLogger(__name__)


def update_requisition(data: dict, **kwargs):
    requisition, update_result = update_local_requisition(data)
    update_remote_requisition(requisition)
    return update_result


def update_local_requisition(data: dict, **kwargs) -> Tuple[Requisition, dict]:
    """Create or update local requisition.
    :parma data: dict with requisition data
    :return: created or updated requisition
    """

    data["external_id"] = data.pop("id")

    patient_data = data.pop("patient")
    patient_data.pop("id")
    patient = Patient.objects.get(birth_number=patient_data["birth_number"])
    data["patient"] = patient

    applicant_data = data.pop("applicant")
    applicant_data.pop("id")
    person_number = applicant_data.pop("person_number")
    applicant, _ = Person.objects.get_or_create(
        person_number=person_number, defaults=applicant_data
    )
    data["applicant"] = applicant

    data["is_synced"] = False
    if data["state"] == Requisition.STATE_CREATED:
        data["state"] = Requisition.STATE_PENDING

    requisition, created = Requisition.objects.update_or_create(
        external_id=data["external_id"], defaults=data
    )
    if created:
        update_result = {"requisitions.Requisition": "created"}
    else:
        update_result = {"requisitions.Requisition": "updated"}

    return requisition, update_result


def update_remote_requisition(
    requisition: Requisition,
    fields_to_update: Union[Iterable, str] = "__all__",
):
    """
    Update remote (izadanky) requisition

    if update is successful, set Requisition.is_synced = True

    :param requisition: Requisition to update
    :param fields_to_update: dict of fields to update, default is all fields ("__all__")
    :return:
    """

    requisition.is_synced = False
    url = settings.UPDATE_REQUISITION_URL.format(id=requisition.external_id)
    headers = {"Authorization": f"Bearer {settings.IZADANKY_TOKEN}"}

    if fields_to_update == "__all__":
        data = {
            "is_synced": True,
            "state": requisition.state,
        }
    else:
        data = {}
        for field in fields_to_update:
            if field not in [f.name for f in Requisition._meta.fields]:
                raise ValueError(f"{field} is not a valid field")
            data[field] = getattr(requisition, field)

    if requisition.solver:
        data["solver"] = requisition.solver.id

    try:
        response = requests.patch(url, data=data, headers=headers)
    except Exception:
        logger.exception(
            f"Remote requisition update failed because of exception",
            extra={"requisition_id": requisition.id},
        )
    else:
        if response.status_code == 200:
            requisition.is_synced = True
            requisition.synced_at = timezone.now()
        else:
            logger.error(
                "Remote requisition update failed because of status code",
                extra={
                    "requisition_id": requisition.id,
                    "response_status_code": response.status_code,
                    "response_text": response.text,
                },
            )

    requisition.save()

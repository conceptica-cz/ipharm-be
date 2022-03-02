from django.utils import timezone
from ipharm.models.cares import Care
from ipharm.models.patients import Patient


def update_names(transformed_data, **kwargs):
    Patient.objects.update_names()


def finish_cares(transformed_data, **kwargs):
    """Finish cares that are not in transformed data."""
    clinic_id = kwargs["url_parameters"]["clinicId"]
    care_ids = []
    for entity in transformed_data:
        if care := entity["care"]:
            care_ids.append(care["external_id"])
    Care.objects.filter(clinic__external_id=clinic_id).exclude(
        external_id__in=care_ids
    ).update(finished_at=timezone.now(), is_active=False)

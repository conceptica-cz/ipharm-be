from collections.abc import Iterable

from references.serializers import PersonSerializer
from rest_framework import serializers
from rest_framework.fields import empty

from ..models.requisitions import Requisition
from .patients import PatientSerializer

COMMON_FIELDS = (
    "id",
    "type",
    "suptype",
    "state",
    "text",
    "applicant",
    "solver",
    "created_at",
    "updated_at",
    "is_synced",
    "synced_at",
)

FIELDS_BY_TYPE = {
    Requisition.TYPE_IPHARM: ("patient", "file"),
    Requisition.TYPE_DELIVERY: (),
}


class RequisitionSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        if instance and not isinstance(instance, Iterable):
            fields = COMMON_FIELDS + FIELDS_BY_TYPE.get(instance.type, ())
        elif data != empty and not isinstance(data, Iterable):
            fields = COMMON_FIELDS + FIELDS_BY_TYPE.get(data.get("type"), ())
        else:
            fields = None
        if fields:
            fields_to_remove = set(self.fields) - set(fields)
            for field in fields_to_remove:
                self.fields.pop(field)

    class Meta:
        model = Requisition
        exclude = ("is_deleted",)
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "patient": {"required": True},
        }


class RequisitionNestedSerializer(RequisitionSerializer):
    patient = PatientSerializer(read_only=True)
    applicant = PersonSerializer(read_only=True)
    solver = PersonSerializer(read_only=True)

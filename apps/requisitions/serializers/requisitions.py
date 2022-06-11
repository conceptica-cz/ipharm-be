from references.serializers import PersonSerializer
from rest_framework import serializers

from ..models.requisitions import Requisition


class RequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        exclude = ("is_deleted",)
        read_only_fields = [
            "id",
            "external_id",
            "type",
            "subtype",
            "text",
            "file_link",
            "applicant",
            "created_at",
            "updated_at",
            "is_synced",
            "synced_at",
        ]


class RequisitionNestedSerializer(RequisitionSerializer):
    applicant = PersonSerializer(read_only=True)
    solver = PersonSerializer(read_only=True)

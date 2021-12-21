from references.models import MedicalFacility
from rest_framework import serializers


class MedicalFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFacility
        exclude = ("is_deleted",)
        read_only_fields = ("id",)

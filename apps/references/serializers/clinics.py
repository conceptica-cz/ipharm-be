from rest_framework import serializers

from ..models.clinics import Clinic, Department


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = read_only_fields = (
            "id",
            "external_id",
            "abbreviation",
            "description",
            "is_hospital",
            "is_ambulance",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = read_only_fields = (
            "id",
            "clinic",
            "clinic_external_id",
            "external_id",
            "abbreviation",
            "description",
        )

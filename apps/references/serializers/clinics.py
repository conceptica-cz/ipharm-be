from rest_framework import serializers

from ..models.clinics import Clinic, Department


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = read_only_fields = (
            "id",
            "identifier",
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
            "clinic_identifier",
            "identifier",
            "abbreviation",
            "description",
        )

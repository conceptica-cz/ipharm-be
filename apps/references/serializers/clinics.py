from rest_framework import serializers

from ..models.clinics import Clinic, Department


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        exclude = ("is_deleted",)
        read_only_fields = ("id",)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ("is_deleted",)
        read_only_fields = ("id",)

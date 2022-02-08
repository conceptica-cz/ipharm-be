from rest_framework import serializers

from ..models.clinics import Clinic, Department


class ClinicSerializer(serializers.ModelSerializer):
    patient_count = serializers.IntegerField(read_only=True)
    patient_without_checkin_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Clinic
        exclude = ("is_deleted",)
        read_only_fields = ("id", "patient_count", "patient_without_checkin_count")


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ("is_deleted", "for_insurance")
        read_only_fields = ("id",)

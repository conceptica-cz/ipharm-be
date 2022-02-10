from ipharm.models import Care, CheckIn, Dekurz
from references.serializers.clinics import ClinicSerializer, DepartmentSerializer
from references.serializers.diagnoses import DiagnosisSerializer
from references.serializers.persons import PersonSerializer
from rest_framework import serializers


class DekurzNestedSerializer(serializers.ModelSerializer):
    doctor = PersonSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)

    class Meta:
        exclude = ["is_deleted"]
        read_only_fields = ["id", "care"]
        model = Dekurz


class CareSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)
        if self.context.get("drop_patient", False):
            self.fields.pop("patient")

    class Meta:
        model = Care
        exclude = ["is_deleted"]
        read_only_fields = ["id", "last_dekurz"]
        extra_kwargs = {"diagnoses": {"required": False, "allow_empty": True}}


class CheckInLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = read_only_fields = ["id", "risk_level"]


class CareNestedSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    main_diagnosis = DiagnosisSerializer(read_only=True)
    last_dekurz = DekurzNestedSerializer(read_only=True)
    checkin = CheckInLiteSerializer(read_only=True)

    class Meta:
        exclude = ["is_deleted"]
        read_only_fields = ["id"]
        model = Care

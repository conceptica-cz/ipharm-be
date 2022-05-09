from ipharm.models.cares import Care, Dekurz
from ipharm.models.checkins import CheckIn
from ipharm.models.pharmacological_plans import PharmacologicalPlan
from ipharm.serializers.checkins import CheckInNestedSerializer
from ipharm.serializers.pharmacological_evaluations import (
    PharmacologicalEvaluationNestedSerializer,
)
from ipharm.serializers.pharmacological_plans import PharmacologicalPlanSerializer
from ipharm.serializers.risk_drug_histories import RiskDrugHistoryNestedSerializer
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
        validators = []

    def validate(self, data):
        care_type = data.get("care_type", Care.HOSPITALIZATION)
        if care_type == Care.HOSPITALIZATION:
            pass
        elif care_type == Care.EXTERNAL:
            if data.get("external_department") is None:
                raise serializers.ValidationError(
                    "external_department must be set for external care"
                )
        return data


class CheckInLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = read_only_fields = [
            "id",
            "risk_level",
            "consultation_requested",
            "pharmacist_intervention_required",
        ]


class PharmacologicalPlanLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacologicalPlan
        fields = read_only_fields = [
            "id",
            "notification_datetime",
        ]


class CareLiteNestedSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    main_diagnosis = DiagnosisSerializer(read_only=True)
    last_dekurz = DekurzNestedSerializer(read_only=True)
    checkin = CheckInLiteSerializer(read_only=True)
    pharmacologicalplan = PharmacologicalPlanLiteSerializer(read_only=True)

    class Meta:
        exclude = ["is_deleted"]
        read_only_fields = ["id"]
        model = Care


class CareNestedSerializer(serializers.ModelSerializer):
    clinic = ClinicSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    main_diagnosis = DiagnosisSerializer(read_only=True)
    last_dekurz = DekurzNestedSerializer(read_only=True)
    checkin = CheckInNestedSerializer(read_only=True)
    pharmacologicalplan = PharmacologicalPlanSerializer(read_only=True)
    riskdrughistory = RiskDrugHistoryNestedSerializer(read_only=True)
    pharmacological_evaluations = PharmacologicalEvaluationNestedSerializer(
        read_only=True, many=True
    )
    patient_informations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        exclude = ["is_deleted"]
        read_only_fields = ["id"]
        model = Care


class CareProceduresSerializer(serializers.Serializer):
    procedure_05751_count = serializers.IntegerField(required=False)
    procedure_05753_count = serializers.IntegerField(required=False)
    procedure_05755_count = serializers.IntegerField(required=False)

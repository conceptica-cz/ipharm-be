from references.serializers.insurances import InsuranceCompanySerializer
from rest_framework import serializers

from ..models.patients import Patient
from .cares import CareLiteNestedSerializer, CareNestedSerializer, CareSerializer


class PatientLiteNestedSerializer(serializers.ModelSerializer):
    insurance_company = InsuranceCompanySerializer(read_only=True)
    current_care = CareLiteNestedSerializer(read_only=True)

    class Meta:
        model = Patient
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PatientNestedSerializer(serializers.ModelSerializer):
    insurance_company = InsuranceCompanySerializer(read_only=True)
    current_care = CareNestedSerializer(read_only=True)

    class Meta:
        model = Patient
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PatientSerializer(serializers.ModelSerializer):
    current_care = CareSerializer(required=False, context={"drop_patient": True})

    class Meta:
        model = Patient
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        if "current_care" in validated_data:
            del validated_data["current_care"]
            care_data = self.initial_data["current_care"]
        else:
            care_data = None

        patient = super().create(validated_data)

        self._save_cares(patient, care_data)
        return patient

    def update(self, instance, validated_data):
        if "current_care" in validated_data:
            del validated_data["current_care"]
            care_data = self.initial_data["current_care"]
        else:
            care_data = None

        patient = super().update(instance, validated_data)

        self._save_cares(patient, care_data)
        return patient

    @staticmethod
    def _save_cares(patient, care_data):
        if care_data:
            care_data["patient"] = patient.pk
            care_serializer = CareSerializer(patient.current_care, data=care_data)
            care_serializer.is_valid(raise_exception=True)
            patient.current_care = care_serializer.save()
            patient.save()

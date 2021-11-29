from references.models import Diagnosis
from references.serializers.insurances import InsuranceCompanySerializer
from rest_framework import serializers

from ..models import Care
from ..models.patients import Patient
from .cares import CareNestedSerializer, CareSerializer


class PatientNestedSerializer(serializers.ModelSerializer):
    insurance_company = InsuranceCompanySerializer(read_only=True)
    current_hospital_care = CareNestedSerializer(read_only=True)
    current_ambulance_care = CareNestedSerializer(read_only=True)

    class Meta:
        model = Patient
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PatientSerializer(serializers.ModelSerializer):
    current_ambulance_care = CareSerializer(
        required=False, context={"drop_patient": True}
    )
    current_hospital_care = CareSerializer(
        required=False, context={"drop_patient": True}
    )

    class Meta:
        model = Patient
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        ambulance_care_data, hospital_care_data = self._extract_care_data(
            validated_data
        )

        patient = super().create(validated_data)

        self._save_cares(patient, ambulance_care_data, hospital_care_data)
        return patient

    def update(self, instance, validated_data):
        ambulance_care_data, hospital_care_data = self._extract_care_data(
            validated_data
        )

        patient = super().update(instance, validated_data)

        self._save_cares(patient, ambulance_care_data, hospital_care_data)
        return patient

    def _extract_care_data(self, validated_data):
        if "current_ambulance_care" in validated_data:
            del validated_data["current_ambulance_care"]
            ambulance_care_data = self.initial_data["current_ambulance_care"]
        else:
            ambulance_care_data = None

        if "current_hospital_care" in validated_data:
            del validated_data["current_hospital_care"]
            hospital_care_data = self.initial_data["current_hospital_care"]
        else:
            hospital_care_data = None
        return ambulance_care_data, hospital_care_data

    def _save_cares(self, patient, ambulance_care_data, hospital_care_data):
        if ambulance_care_data:
            ambulance_care_data["patient"] = patient.pk
            ambulance_care_data["care_type"] = Care.AMBULATION
            care_serializer = CareSerializer(
                patient.current_ambulance_care, data=ambulance_care_data
            )
            care_serializer.is_valid(raise_exception=True)
            patient.current_ambulance_care = care_serializer.save()
            patient.save()

        if hospital_care_data:
            hospital_care_data["patient"] = patient.pk
            hospital_care_data["care_type"] = Care.HOSPITALIZATION
            care_serializer = CareSerializer(
                patient.current_hospital_care, data=hospital_care_data
            )
            care_serializer.is_valid(raise_exception=True)
            patient.current_hospital_care = care_serializer.save()
            patient.save()

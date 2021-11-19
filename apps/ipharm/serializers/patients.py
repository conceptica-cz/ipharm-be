from references.models import Diagnosis
from references.serializers.insurances import InsuranceCompanySerializer
from rest_framework import serializers

from ..models.patients import Patient
from .cares import CareNestedSerializer


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ["is_deleted", "update"]
        read_only_fields = ["id"]


class PatientNestedSerializer(serializers.ModelSerializer):
    insurance_company = InsuranceCompanySerializer(read_only=True)
    current_hospital_care = CareNestedSerializer(read_only=True)
    current_ambulance_care = CareNestedSerializer(read_only=True)

    class Meta:
        model = Patient
        exclude = ["is_deleted", "update"]
        read_only_fields = ["id"]

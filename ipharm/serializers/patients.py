from rest_framework import serializers

from ..models import patients


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = patients.Clinic
        fields = ["id", "clinic_type", "clinic_id", "abbreviation", "description"]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = patients.Patient
        fields = "__all__"

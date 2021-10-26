from rest_framework import serializers

from ..models.clinics import Clinic


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ["id", "clinic_type", "clinic_id", "abbreviation", "description"]

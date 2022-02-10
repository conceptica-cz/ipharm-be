from references.models import Diagnosis
from rest_framework import serializers


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = read_only_fields = ("id", "code", "name")

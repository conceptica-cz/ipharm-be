from references.models import Diagnosis
from rest_framework import serializers


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        exclude = ("is_deleted",)
        read_only_fields = ("id",)

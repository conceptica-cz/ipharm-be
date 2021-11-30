from ipharm.models import RiskDrugHistory
from references.serializers import DiagnosisSerializer, DrugSerializer, TagSerializer
from rest_framework import serializers


class RiskDrugHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDrugHistory
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class RiskDrugHistoryNestedSerializer(serializers.ModelSerializer):
    risk_drugs = DrugSerializer(many=True, read_only=True)
    risk_risk_diagnoses = DiagnosisSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = RiskDrugHistory
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

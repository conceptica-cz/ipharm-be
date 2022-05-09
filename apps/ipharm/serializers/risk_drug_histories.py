from ipharm.models.risk_drug_histories import (
    RiskDrugHistory,
    RiskDrugHistoryComment,
    RiskDrugHistoryDiagnosis,
)
from references.serializers import DiagnosisSerializer, DrugSerializer, TagSerializer
from rest_framework import serializers


class RiskDrugHistoryDiagnosisNestedSerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many=True, read_only=True)
    diagnosis = DiagnosisSerializer()

    class Meta:
        model = RiskDrugHistoryDiagnosis
        exclude = ("is_deleted",)


class RiskDrugHistoryDiagnosisSerializer(serializers.ModelSerializer):
    drugs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DrugSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )

    class Meta:
        model = RiskDrugHistoryDiagnosis
        exclude = ("is_deleted",)


class RiskDrugHistoryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDrugHistoryComment
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class RiskDrugHistorySerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TagSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )

    class Meta:
        model = RiskDrugHistory
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class RiskDrugHistoryNestedSerializer(serializers.ModelSerializer):
    diagnoses = RiskDrugHistoryDiagnosisNestedSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = RiskDrugHistoryCommentSerializer(many=True, read_only=True)

    class Meta:
        model = RiskDrugHistory
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

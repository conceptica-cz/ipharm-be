from ipharm.models.risk_drug_histories import RiskDrugHistory, RiskDrugHistoryComment
from references.serializers import DiagnosisSerializer, DrugSerializer, TagSerializer
from rest_framework import serializers


class RiskDrugHistoryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskDrugHistoryComment
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class RiskDrugHistorySerializer(serializers.ModelSerializer):
    risk_drugs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DrugSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )
    risk_diagnoses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DiagnosisSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )
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
    risk_drugs = DrugSerializer(many=True, read_only=True)
    risk_risk_diagnoses = DiagnosisSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = RiskDrugHistoryCommentSerializer(many=True, read_only=True)

    class Meta:
        model = RiskDrugHistory
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

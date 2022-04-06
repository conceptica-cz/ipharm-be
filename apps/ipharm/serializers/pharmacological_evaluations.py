from ipharm.models.pharmacological_evaluations import (
    PharmacologicalEvaluation,
    PharmacologicalEvaluationComment,
)
from references.serializers import DrugSerializer, TagSerializer
from rest_framework import serializers


class PharmacologicalEvaluationSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TagSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )

    class Meta:
        model = PharmacologicalEvaluation
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PharmacologicalEvaluationNestedSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    drug = DrugSerializer(read_only=True)

    class Meta:
        model = PharmacologicalEvaluation
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PharmacologicalEvaluationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacologicalEvaluationComment
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

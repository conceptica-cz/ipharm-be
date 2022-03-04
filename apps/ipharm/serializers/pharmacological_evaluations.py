from ipharm.models.pharmacological_evaluations import (
    PharmacologicalEvaluation,
    PharmacologicalEvaluationComment,
)
from references.serializers import TagSerializer
from rest_framework import serializers


class PharmacologicalEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacologicalEvaluation
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PharmacologicalEvaluationNestedSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = PharmacologicalEvaluation
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PharmacologicalEvaluationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacologicalEvaluationComment
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

from ipharm.models import PharmacologicalEvaluation
from references.serializers import DiagnosisSerializer, DrugSerializer, TagSerializer
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

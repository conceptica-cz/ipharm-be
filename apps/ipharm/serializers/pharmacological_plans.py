from ipharm.models import PharmacologicalPlan
from references.serializers import DiagnosisSerializer, DrugSerializer, TagSerializer
from rest_framework import serializers


class PharmacologicalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacologicalPlan
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PharmacologicalPlanNestedSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = PharmacologicalPlan
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

from ipharm.models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)
from references.serializers import TagSerializer
from rest_framework import serializers


class PharmacologicalPlanCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacologicalPlanComment
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PharmacologicalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacologicalPlan
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PharmacologicalPlanNestedSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = PharmacologicalPlanCommentSerializer(many=True, read_only=True)

    class Meta:
        model = PharmacologicalPlan
        fields = [
            "id",
            "care",
            "text",
            "his_text",
            "note",
            "notification_datetime",
            "tags",
            "comments",
        ]
        read_only_fields = ["id"]

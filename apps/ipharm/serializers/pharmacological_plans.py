from ipharm.models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)
from references.serializers import TagSerializer
from rest_framework import serializers, status


class PharmacologicalPlanCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacologicalPlanComment
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

    def validate(self, data):
        if self.instance:
            pharmacological_plan = self.instance.pharmacological_plan
        else:
            pharmacological_plan = data["pharmacological_plan"]

        if (
            PharmacologicalPlanComment.objects.filter(
                pharmacological_plan=pharmacological_plan,
                comment_type=PharmacologicalPlanComment.VERIFICATION,
            ).count()
            >= 2
        ):
            raise serializers.ValidationError(
                "Verification comments are limited to 2 per plan.",
                code="VerificationNumberLimitIsReached",
            )
        return data


class PharmacologicalPlanSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TagSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )

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

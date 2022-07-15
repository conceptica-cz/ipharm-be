from ipharm.models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)
from references.serializers import TagSerializer
from rest_framework import serializers, status
from users.serializers import UserLightSerializer


class PharmacologicalPlanCommentSerializer(serializers.ModelSerializer):
    author = UserLightSerializer(read_only=True)

    class Meta:
        model = PharmacologicalPlanComment
        exclude = ["is_deleted"]
        read_only_fields = ["id", "author"]

    def validate(self, data):
        if self.instance:
            pharmacological_plan = self.instance.pharmacological_plan
            comment_type = self.instance.comment_type
        else:
            pharmacological_plan = data["pharmacological_plan"]
            comment_type = data.get("comment_type", PharmacologicalPlanComment.COMMENT)

        if (
            PharmacologicalPlanComment.objects.filter(
                pharmacological_plan=pharmacological_plan,
                comment_type=PharmacologicalPlanComment.VERIFICATION,
            ).count()
            >= 2
            and comment_type == PharmacologicalPlanComment.VERIFICATION
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

from ipharm.models.checkins import CheckIn
from references.serializers import DiagnosisSerializer
from references.serializers.drugs import DrugSerializer
from rest_framework import serializers


class CheckInSerializer(serializers.ModelSerializer):
    drugs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DrugSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )
    high_interaction_potential_drugs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DrugSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )
    diagnoses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DiagnosisSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )
    diagnoses_drugs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DrugSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )
    narrow_therapeutic_window_drugs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DrugSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )

    class Meta:
        model = CheckIn
        exclude = ["is_deleted"]
        read_only_fields = ["id", "medical_procedure"]


class CheckInNestedSerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many=True, read_only=True)
    high_interaction_potential_drugs = DrugSerializer(many=True, read_only=True)
    diagnoses = DiagnosisSerializer(many=True, read_only=True)
    diagnoses_drugs = DrugSerializer(many=True, read_only=True)
    narrow_therapeutic_window_drugs = DrugSerializer(many=True, read_only=True)

    class Meta:
        model = CheckIn
        exclude = ["is_deleted"]
        read_only_fields = ["id", "medical_procedure"]

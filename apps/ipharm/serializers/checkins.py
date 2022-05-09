from ipharm.models.checkins import CheckIn, CheckInDiagnosis, CheckInDiagnosisDrug
from references.serializers import DiagnosisSerializer
from references.serializers.drugs import DrugSerializer
from rest_framework import serializers


class CheckInDiagnosisNestedSerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many=True, read_only=True)
    diagnosis = DiagnosisSerializer()

    class Meta:
        model = CheckInDiagnosis
        exclude = ("is_deleted",)


class CheckInDiagnosisSerializer(serializers.ModelSerializer):
    drugs = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DrugSerializer.Meta.model.objects.all(),
        allow_empty=True,
        required=False,
    )

    class Meta:
        model = CheckInDiagnosis
        exclude = ("is_deleted",)


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
    diagnoses = CheckInDiagnosisNestedSerializer(many=True, read_only=True)
    narrow_therapeutic_window_drugs = DrugSerializer(many=True, read_only=True)

    class Meta:
        model = CheckIn
        exclude = ["is_deleted"]
        read_only_fields = ["id", "medical_procedure"]

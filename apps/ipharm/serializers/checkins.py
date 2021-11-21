from ipharm.models import CheckIn
from references.serializers.drugs import DrugSerializer
from rest_framework import serializers


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        exclude = ["is_deleted", "update"]
        read_only_fields = ["id"]


class CheckInNestedSerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many=True, read_only=True)
    high_interaction_potential_drugs = DrugSerializer(many=True, read_only=True)
    narrow_therapeutic_window_drugs = DrugSerializer(many=True, read_only=True)

    class Meta:
        model = CheckIn
        exclude = ["is_deleted", "update"]
        read_only_fields = ["id"]

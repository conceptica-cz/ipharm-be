from ipharm.models import PatientInformation
from rest_framework import serializers


class PatientInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInformation
        exclude = ["is_deleted"]
        read_only_fields = ["id"]


class PatientInformationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInformation
        exclude = ["is_deleted"]
        read_only_fields = ["id"]

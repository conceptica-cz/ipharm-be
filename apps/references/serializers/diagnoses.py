from references.models import Diagnosis
from rest_framework import serializers


class DiagnosisListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        return [Diagnosis.objects.create(**item) for item in validated_data]

    def update(self, instance, validated_data):
        """Update diagnoses

        Delete all existing diagnoses, except for those received via external API,
        and create new ones from validated_data.
        """
        instance.exclude(patientdiagnosis__via_api=True).delete()


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = read_only_fields = ("id", "code", "name")


#        list_serializer_class = DiagnosisListSerializer

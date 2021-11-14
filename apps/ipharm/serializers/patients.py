from references.models import Diagnosis
from references.serializers.clinics import DepartmentSerializer
from references.serializers.diagnoses import DiagnosisSerializer
from references.serializers.insurances import InsuranceCompanySerializer
from references.serializers.persons import PersonSerializer
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from ..models.patients import Patient


class PatientSerializer(serializers.ModelSerializer):
    diagnoses = PrimaryKeyRelatedField(many=True, queryset=Diagnosis.objects.all())

    class Meta:
        model = Patient
        fields = [
            "id",
            "clinic",
            "patient_type",
            "record_id",
            "patient_id",
            "first_name",
            "last_name",
            "birth_date",
            "birth_number",
            "insurance_company",
            "insurance_number",
            "height",
            "weight",
            "department_in",
            "datetime_in",
            "datetime_out",
            "diagnoses",
            "dekurz_datetime",
            "dekurz_who",
            "dekurz_department",
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr != "diagnoses":
                setattr(instance, attr, value)
        instance.save()
        instance.update_diagnoses(validated_data["diagnoses"])
        return instance


class PatientNestedSerializer(serializers.ModelSerializer):
    insurance_company = InsuranceCompanySerializer(read_only=True)
    department_in = DepartmentSerializer(read_only=True)
    diagnoses = DiagnosisSerializer(read_only=True, many=True)
    dekurz_department = DepartmentSerializer(read_only=True)
    dekurz_who = PersonSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "clinic",
            "patient_type",
            "record_id",
            "patient_id",
            "first_name",
            "last_name",
            "birth_date",
            "birth_number",
            "insurance_company",
            "insurance_number",
            "height",
            "weight",
            "department_in",
            "datetime_in",
            "datetime_out",
            "diagnoses",
            "dekurz_datetime",
            "dekurz_who",
            "dekurz_department",
        ]
        read_only_fields = ["id"]

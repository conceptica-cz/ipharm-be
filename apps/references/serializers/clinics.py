from rest_framework import serializers

from ..models.clinics import Clinic, Department, Person


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = read_only_fields = (
            "id",
            "clinic_id",
            "abbreviation",
            "description",
            "is_hospital",
            "is_ambulance",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = read_only_fields = (
            "id",
            "clinic",
            "department_id",
            "abbreviation",
            "description",
        )


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = read_only_fields = (
            "id",
            "person_number",
            "name",
            "f_title",
            "l_title",
        )

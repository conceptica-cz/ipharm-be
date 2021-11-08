from references.models import InsuranceCompany
from rest_framework import serializers


class InsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCompany
        fields = ["id", "code", "name"]
        read_only_fields = ("id",)

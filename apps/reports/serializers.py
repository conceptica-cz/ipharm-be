from reports.models import GenericReportFile, GenericReportType, ReportVariable
from rest_framework.serializers import ModelSerializer, ValidationError


class GenericReportTypeSerializer(ModelSerializer):
    class Meta:
        model = GenericReportType
        fields = "__all__"
        read_only_fields = [field.name for field in model._meta.fields]


class GenericReportFileSerializer(ModelSerializer):
    class Meta:
        model = GenericReportFile
        fields = read_only_fields = ("file", "created_at", "updated_at")


class ReportVariableSerializer(ModelSerializer):
    class Meta:
        model = ReportVariable
        fields = (
            "id",
            "name",
            "description",
            "variable_type",
            "value",
            "order",
        )
        read_only_fields = [field for field in fields if field != "value"]

    def validate(self, data):
        variable_type = self.instance.variable_type
        caster = ReportVariable.CASTERS[variable_type]
        try:
            caster(data["value"])
        except ValueError:
            raise ValidationError(
                "Invalid value for variable type '{}'".format(variable_type)
            )
        return data

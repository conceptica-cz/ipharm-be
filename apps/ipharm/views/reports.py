from references.managers.departments import DepartmentForReportNotFound
from references.managers.identifications import IdentificationForReportNotFound
from reports.models import GenericReportType, ReportVariable
from reports.serializers import (
    GenericReportFileSerializer,
    GenericReportTypeSerializer,
    ReportVariableSerializer,
)
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


class GenericReportTypeListView(generics.ListAPIView):
    queryset = GenericReportType.objects.all()
    serializer_class = GenericReportTypeSerializer


class ReportVariableListView(generics.ListAPIView):
    serializer_class = ReportVariableSerializer

    def get_queryset(self):
        return ReportVariable.objects.filter(report_type=self.kwargs["pk"])


class ReportVariableDetailView(generics.RetrieveUpdateAPIView):
    queryset = ReportVariable.objects.all()
    serializer_class = ReportVariableSerializer


class ReportGenerateView(APIView):
    def get(self, request, *args, **kwargs):
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        report_type = GenericReportType.objects.get(pk=self.kwargs["pk"])
        try:
            report_file = report_type.generate_report(year=year, month=month)
        except IdentificationForReportNotFound:
            raise serializers.ValidationError(
                "Identification for report not found. Please, add it. Dont forget to set for_for_insurance=True.",
                code="IdentificationForReportNotFound",
            )
        except DepartmentForReportNotFound:
            raise serializers.ValidationError(
                "Department for report not found. Please, add it. Dont forget to set for_for_insurance=True.",
                code="DepartmentForReportNotFound",
            )
        response = Response(GenericReportFileSerializer(report_file).data)
        return response

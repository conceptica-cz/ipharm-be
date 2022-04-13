from django.utils import dateparse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
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


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="report_format",
                type=OpenApiTypes.STR,
                enum=["pdf", "xsls"],
                location=OpenApiParameter.QUERY,
                description="Report file format. Not all formats are available for every report. Value must be from the report's field ``formats``",  # noqa
            ),
            OpenApiParameter(
                name="time_range",
                type=OpenApiTypes.DATE,
                enum=["year", "month", "custom"],
                location=OpenApiParameter.QUERY,
                description="Type of report time interval. Not all time intervals available for every report. Value must be from the report's field ``time_ranges``",  # noqa
            ),
            OpenApiParameter(
                name="year",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="From date (only if parameter ``time_range`` is **month**).",
            ),
            OpenApiParameter(
                name="month",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="From date (only if parameter ``time_range`` is **year** or **month**).",
            ),
            OpenApiParameter(
                name="date_to",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="From date (only if parameter ``time_range`` is **custom**)",
            ),
            OpenApiParameter(
                name="date_to",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="To date (only if parameter ``time_range`` is **custom**)",
            ),
            OpenApiParameter(
                name="clinic",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="The ID of the clinic used as filter. Not all filters available for every report. **clinic** must be in the report's field ``filters``",  # noqa
            ),
            OpenApiParameter(
                name="department",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="The ID of the department used as filter. Not all filters available for every report. **department** must be in the report's field ``filters``",  # noqa
            ),
        ]
    )
)
class ReportGenerateView(APIView):
    def get(self, request, *args, **kwargs):
        report_format = self.request.query_params.get("report_format")
        time_range = self.request.query_params.get("time_range")
        year = self.request.query_params.get("year")
        month = self.request.query_params.get("month")
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        report_type = GenericReportType.objects.get(pk=self.kwargs["pk"])
        NO_FILTER_PARAMS = (
            "report_format",
            "time_range",
            "year",
            "month",
            "date_from",
            "date_to",
        )
        filters = {
            k: v
            for k, v in self.request.query_params.items()
            if k not in NO_FILTER_PARAMS
        }
        if year is not None:
            try:
                year = int(year)
            except ValueError:
                return Response(
                    {"error": "Invalid year value. Must be an integer."}, status=400
                )
        if month is not None:
            try:
                month = int(month)
            except ValueError:
                return Response(
                    {"error": "Invalid month value. Must be an integer."}, status=400
                )
        if date_from is not None:
            datetime_from = dateparse.parse_date(date_from)
            if datetime_from is None:
                return Response({"error": "Invalid date_from."}, status=400)
        if date_to is not None:
            datet_to = dateparse.parse_datetime(date_to)
            if date_to is None:
                return Response({"error": "Invalid date_to."}, status=400)
        try:
            report_file = report_type.generate_report(
                report_format=report_format,
                time_range=time_range,
                year=year,
                month=month,
                date_from=date_from,
                date_to=date_to,
                filters=filters,
            )
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

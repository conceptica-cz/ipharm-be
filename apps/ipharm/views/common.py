from django.utils import dateparse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import views
from rest_framework.response import Response
from updates.serializers import ModelChangeSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="from",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="From datetime",
            ),
            OpenApiParameter(
                name="to",
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                description="To datetime",
            ),
        ]
    )
)
class HistoryView(views.APIView):
    queryset = None

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        obj = self.queryset.get(pk=pk)
        datetime_from = request.query_params.get("from")
        datetime_to = request.query_params.get("to")
        if datetime_from:
            datetime_from = dateparse.parse_datetime(datetime_from)
            if datetime_from is None:
                return Response(
                    {"error": "Invalid datetime_from. Use ISO 8601 format."}, status=400
                )
        if datetime_to:
            datetime_to = dateparse.parse_datetime(datetime_to)
            if datetime_to is None:
                return Response(
                    {"error": "Invalid datetime_to. Use ISO 8601 format."}, status=400
                )
        changes = obj.get_merged_changes(datetime_from, datetime_to)
        serializer = ModelChangeSerializer(changes, many=True)
        return Response(serializer.data)

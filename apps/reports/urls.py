from django.urls import path

from .views import reports

app_name = "reports"

urlpatterns = [
    path(
        "reports/",
        reports.GenericReportTypeListView.as_view(),
        name="report_list",
    ),
    path(
        "reports/<int:pk>/variables/",
        reports.ReportVariableListView.as_view(),
        name="report_variable_list",
    ),
    path(
        "reports/<int:pk>/generate/",
        reports.ReportGenerateView.as_view(),
        name="report_generate",
    ),
    path(
        "report-variables/<int:pk>/",
        reports.ReportVariableDetailView.as_view(),
        name="report_variable_detail",
    ),
]

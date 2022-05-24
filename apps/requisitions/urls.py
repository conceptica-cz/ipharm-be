from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import patients, requisitions

app_name = "requisitions"

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="requisitions:schema"),
        name="swagger-ui",
    ),
    path(
        "requisitions/",
        requisitions.RequisitionListView.as_view(),
        name="requisition_list",
    ),
    path(
        "requisitions/<int:pk>/",
        requisitions.RequisitionDetailView.as_view(),
        name="requisition_detail",
    ),
    path(
        "requisitions/<int:pk>/history/",
        requisitions.RequisitionHistoryView.as_view(),
        name="requisition_history",
    ),
    path(
        "patients/",
        patients.PatientListView.as_view(),
        name="patient_list",
    ),
    path(
        "patients/load-patient/",
        patients.PatientLoadView.as_view(),
        name="patient_load",
    ),
    path(
        "patients/<int:pk>/",
        patients.PatientDetailView.as_view(),
        name="patient_detail",
    ),
    path(
        "patients/<int:pk>/history/",
        patients.PatientHistoryView.as_view(),
        name="patient_history",
    ),
]

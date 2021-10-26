from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import patients, user

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("user/", user.UserView.as_view(), name="user"),
    path("clinics/", patients.ClinicListView.as_view(), name="clinic_list"),
    path(
        "clinics/<int:pk>/", patients.ClinicDetailView.as_view(), name="clinic_detail"
    ),
    path("patients/", patients.PatientListView.as_view(), name="patient_list"),
    path(
        "patients/<int:pk>/",
        patients.PatientDetailView.as_view(),
        name="patient_detail",
    ),
]

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import cares, checkins, clinics, patients, user

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("user/", user.UserView.as_view(), name="user"),
    path("clinics/", clinics.ClinicListView.as_view(), name="clinic_list"),
    path("clinics/<int:pk>/", clinics.ClinicDetailView.as_view(), name="clinic_detail"),
    path("patients/", patients.PatientListView.as_view(), name="patient_list"),
    path(
        "patients/<int:pk>/",
        patients.PatientDetailView.as_view(),
        name="patient_detail",
    ),
    path(
        "patients/<int:patient_pk>/current_hospital_care/",
        cares.PatientCareDetailView.as_view(),
        {"care_type": "hospital"},
        name="patient_current_hospital_care",
    ),
    path(
        "patients/<int:patient_pk>/current_ambulance_care/",
        cares.PatientCareDetailView.as_view(),
        {"care_type": "ambulance"},
        name="patient_current_ambulance_care",
    ),
    path(
        "cares/<int:pk>/",
        cares.CareDetailView.as_view(),
        name="care_detail",
    ),
    path("checkins/", checkins.CheckInListView.as_view(), name="checkin_list"),
    path(
        "checkins/<int:pk>/",
        checkins.CheckInDetailView.as_view(),
        name="checkin_detail",
    ),
]

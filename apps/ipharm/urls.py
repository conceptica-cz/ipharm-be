from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import (
    cares,
    checkins,
    clinics,
    patient_informations,
    patients,
    pharmacological_evaluations,
    pharmacological_plans,
    risk_drug_histories,
    user,
)

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
    path(
        "risk-drug-histories/",
        risk_drug_histories.RiskDrugHistoryListView.as_view(),
        name="risk_drug_history_list",
    ),
    path(
        "risk-drug-histories/<int:pk>/",
        risk_drug_histories.RiskDrugHistoryDetailView.as_view(),
        name="risk_drug_history_detail",
    ),
    path(
        "risk-drug-history-comments/",
        risk_drug_histories.RiskDrugHistoryCommentListView.as_view(),
        name="risk_drug_history_comment_list",
    ),
    path(
        "risk-drug-history-comments/<int:pk>/",
        risk_drug_histories.RiskDrugHistoryCommentDetailView.as_view(),
        name="risk_drug_history_comment_detail",
    ),
    path(
        "patient-informations/",
        patient_informations.PatientInformationListView.as_view(),
        name="patient_information_list",
    ),
    path(
        "patient-informations/<int:pk>/",
        patient_informations.PatientInformationDetailView.as_view(),
        name="patient_information_detail",
    ),
    path(
        "patient-informations/",
        patient_informations.PatientInformationListView.as_view(),
        name="patient_information_list",
    ),
    path(
        "patient-informations/<int:pk>/",
        patient_informations.PatientInformationDetailView.as_view(),
        name="patient_information_detail",
    ),
    path(
        "pharmacological-evaluations/",
        pharmacological_evaluations.PharmacologicalEvaluationListView.as_view(),
        name="pharmacological_evaluation_list",
    ),
    path(
        "pharmacological-evaluations/<int:pk>/",
        pharmacological_evaluations.PharmacologicalEvaluationDetailView.as_view(),
        name="pharmacological_evaluation_detail",
    ),
    path(
        "pharmacological-plans/",
        pharmacological_plans.PharmacologicalPlanListView.as_view(),
        name="pharmacological_plan_list",
    ),
    path(
        "pharmacological-plans/<int:pk>/",
        pharmacological_plans.PharmacologicalPlanDetailView.as_view(),
        name="pharmacological_plan_detail",
    ),
    path(
        "pharmacological-plan-comments/",
        pharmacological_plans.PharmacologicalPlanCommentListView.as_view(),
        name="pharmacological_plan_comment_list",
    ),
    path(
        "pharmacological-plan-comments/<int:pk>/",
        pharmacological_plans.PharmacologicalPlanCommentDetailView.as_view(),
        name="pharmacological_plan_comment_detail",
    ),
]

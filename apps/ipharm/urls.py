from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import (
    cares,
    checkins,
    clinics,
    diagnoses,
    drugs,
    facilities,
    insurances,
    patient_informations,
    patients,
    persons,
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
    path("departments/", clinics.DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/<int:pk>/",
        clinics.DepartmentDetailView.as_view(),
        name="department_detail",
    ),
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
    path("persons/", persons.PersonListView.as_view(), name="person_list"),
    path("persons/<int:pk>/", persons.PersonDetailView.as_view(), name="person_detail"),
    path("diagnoses/", diagnoses.DiagnosisListView.as_view(), name="diagnosis_list"),
    path(
        "diagnoses/<int:pk>/",
        diagnoses.DiagnosisDetailView.as_view(),
        name="diagnosis_detail",
    ),
    path("drugs/", drugs.DrugListView.as_view(), name="drug_list"),
    path(
        "drugs/<int:pk>/",
        drugs.DrugDetailView.as_view(),
        name="drug_detail",
    ),
    path(
        "insurances/",
        insurances.InsuranceCompanyListView.as_view(),
        name="insurance_company_list",
    ),
    path(
        "insurances/<int:pk>/",
        insurances.InsuranceCompanyDetailView.as_view(),
        name="insurance_company_detail",
    ),
    path(
        "facilities/",
        facilities.MedicalFacilityListView.as_view(),
        name="medical_facility_list",
    ),
    path(
        "facilities/<int:pk>/",
        facilities.MedicalFacilityDetailView.as_view(),
        name="medical_facility_detail",
    ),
]

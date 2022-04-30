from django.urls import path

from .views import (
    clinics,
    diagnoses,
    drugs,
    external_departments,
    facilities,
    insurances,
    persons,
    tags,
)

app_name = "references"

urlpatterns = [
    path("clinics/", clinics.ClinicListView.as_view(), name="clinic_list"),
    path("clinics/<int:pk>/", clinics.ClinicDetailView.as_view(), name="clinic_detail"),
    path("departments/", clinics.DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/<int:pk>/",
        clinics.DepartmentDetailView.as_view(),
        name="department_detail",
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
        "external_departments/",
        external_departments.ExternalDepartmentListView.as_view(),
        name="external_department_list",
    ),
    path(
        "external_departments/<int:pk>/",
        external_departments.ExternalDepartmentDetailView.as_view(),
        name="external_department_detail",
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
    path(
        "tags/",
        tags.TagListView.as_view(),
        name="tag_list",
    ),
    path(
        "tags/<int:pk>/",
        tags.TagDetailView.as_view(),
        name="tag_detail",
    ),
]

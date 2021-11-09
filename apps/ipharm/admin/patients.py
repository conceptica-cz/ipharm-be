from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models import patients


class PatientDiagnosisInline(admin.TabularInline):
    model = patients.PatientDiagnosis
    extra = 1


@admin.register(patients.Patient)
class PatientAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "last_name",
        "first_name",
        "clinic",
        "patient_type",
        "birth_number",
        "is_deleted",
    ]
    search_fields = ["birth_number", "last_name"]
    list_filter = ["clinic", "patient_type"]
    inlines = [PatientDiagnosisInline]

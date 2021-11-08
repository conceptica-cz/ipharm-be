from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from ..models import patients


class PatientDiagnosisInline(admin.TabularInline):
    model = patients.PatientDiagnosis
    extra = 1


@admin.register(patients.Patient)
class PatientAdmin(SimpleHistoryAdmin):
    list_display = [
        "pk",
        "last_name",
        "first_name",
        "clinic",
        "patient_type",
        "birth_number",
    ]
    search_fields = ["birth_number", "last_name"]
    list_filter = ["clinic", "patient_type"]
    inlines = [PatientDiagnosisInline]

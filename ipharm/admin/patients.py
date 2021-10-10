from django.contrib import admin

from ..models import patients


@admin.register(patients.Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ["clinic_id", "description", "abbreviation"]


@admin.register(patients.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["clinic", "last_name", "first_name", "birth_number"]
    search_fields = ["birth_number", "last_name"]
    list_filter = ["clinic"]

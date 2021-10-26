from django.contrib import admin

from ..models.clinics import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ["pk", "clinic_type", "clinic_id", "description", "abbreviation"]
    list_filter = ["clinic_type"]

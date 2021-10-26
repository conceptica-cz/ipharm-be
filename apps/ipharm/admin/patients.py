from django.contrib import admin

from ..models import patients


@admin.register(patients.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["pk", "last_name", "first_name", "clinic", "birth_number"]
    search_fields = ["birth_number", "last_name"]
    list_filter = ["clinic"]

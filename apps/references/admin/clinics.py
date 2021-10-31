from django.contrib import admin
from references import models
from simple_history.admin import SimpleHistoryAdmin


@admin.register(models.Clinic)
class ClinicAdmin(SimpleHistoryAdmin):
    list_display = ["pk", "clinic_type", "clinic_id", "description", "abbreviation"]
    list_filter = ["clinic_type"]

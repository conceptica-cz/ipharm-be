from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.Clinic)
class ClinicAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "identifier",
        "description",
        "abbreviation",
        "is_hospital",
        "is_ambulance",
    ]
    search_fields = ["identifier", "description", "abbreviation"]


@admin.register(models.Department)
class DepartmentAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "identifier",
        "description",
        "abbreviation",
        "clinic",
        "clinic_identifier",
    ]
    search_fields = ["identifier", "description", "abbreviation"]
    list_filter = ["clinic"]

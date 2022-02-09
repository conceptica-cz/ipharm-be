from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.Clinic)
class ClinicAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "external_id",
        "description",
        "abbreviation",
        "is_hospital",
        "is_ambulance",
    ]
    search_fields = ["external_id", "description", "abbreviation"]


@admin.register(models.Department)
class DepartmentAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "external_id",
        "description",
        "abbreviation",
        "clinic",
        "for_insurance",
    ]
    search_fields = ["external_id", "description", "abbreviation"]
    list_filter = ["clinic"]

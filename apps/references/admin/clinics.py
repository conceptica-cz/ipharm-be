from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.Clinic)
class ClinicAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "clinic_id",
        "description",
        "abbreviation",
        "is_hospital",
        "is_ambulance",
    ]
    search_fields = ["clinic_id", "description", "abbreviation"]


@admin.register(models.Department)
class DepartmentAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "department_id",
        "description",
        "abbreviation",
        "clinic",
    ]
    search_fields = ["department_id", "description", "abbreviation"]
    list_filter = ["clinic"]


@admin.register(models.Person)
class PersonAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "person_number",
        "name",
        "f_title",
        "l_title",
    ]
    search_fields = ["person_number", "name"]

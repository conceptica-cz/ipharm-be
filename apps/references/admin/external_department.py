from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.ExternalDepartment)
class ExternalDepartmentAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "icp",
        "organization",
        "department",
        "specialization_code",
    ]
    search_fields = ["icp", "organization"]

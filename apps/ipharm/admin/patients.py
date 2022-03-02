from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.patients import Patient


@admin.register(Patient)
class PatientAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "name",
        "birth_number",
        "external_id",
        "created_at",
        "updated_at",
    ]
    search_fields = ["birth_number", "name", "external_id"]

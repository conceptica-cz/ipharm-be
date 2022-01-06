from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models import patients


@admin.register(patients.Patient)
class PatientAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "last_name",
        "first_name",
        "birth_number",
        "external_id",
        "created_at",
        "updated_at",
    ]
    search_fields = ["birth_number", "last_name", "external_id"]

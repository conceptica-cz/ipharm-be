from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.cares import Care


@admin.register(Care)
class CareAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "external_id",
        "care_type",
        "clinic",
        "patient",
        "started_at",
        "finished_at",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_select_related = ["patient"]
    search_fields = ["patient__name", "patient__birth_number", "external_id"]
    list_filter = ["care_type", "is_active"]
    autocomplete_fields = ("main_diagnosis",)

    exclude = ["dekurzes"]

from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.requisitions import Requisition


@admin.register(Requisition)
class RequisitionAdmin(BaseHistoryAdmin):
    list_display = [
        "id",
        "external_id",
        "type",
        "subtype",
        "state",
        "applicant",
        "solver",
        "created_at",
        "updated_at",
        "is_synced",
        "synced_at",
    ]
    list_filter = ["type", "subtype", "state", "applicant"]
    search_fields = ["id"]

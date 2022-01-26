from common.admin import BaseHistoryAdmin
from django.contrib import admin

from .. import models


@admin.register(models.Care)
class CareAdmin(BaseHistoryAdmin):
    list_display = ["pk", "external_id", "care_type", "patient", "is_active"]
    list_select_related = ["patient"]
    list_filter = ["care_type", "is_active", "patient"]
    autocomplete_fields = ("main_diagnosis",)

    exclude = ["dekurzes"]

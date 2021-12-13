from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.Drug)
class DrugAdmin(BaseHistoryAdmin):
    list_display = [
        "code_sukl",
        "name",
        "name_supplement",
        "atc_group",
    ]
    search_fields = ["code_sukl", "name"]

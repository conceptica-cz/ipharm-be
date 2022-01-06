from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.MedicalProcedure)
class MedicalProcedureAdmin(BaseHistoryAdmin):
    list_display = ["code", "name", "scores"]
    search_fields = [
        "code",
        "name",
    ]

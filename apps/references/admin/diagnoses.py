from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.Diagnosis)
class DiagnosisAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "code",
        "name",
    ]
    search_fields = [
        "code",
        "name",
    ]

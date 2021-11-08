from django.contrib import admin
from references import models
from simple_history.admin import SimpleHistoryAdmin


@admin.register(models.Diagnosis)
class DiagnosisAdmin(SimpleHistoryAdmin):
    list_display = [
        "pk",
        "code",
        "name",
    ]
    search_fields = [
        "code",
        "name",
    ]

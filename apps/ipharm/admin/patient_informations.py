from common.admin import BaseHistoryAdmin
from django.contrib import admin

from .. import models


@admin.register(models.PatientInformation)
class PatientInformationAdmin(BaseHistoryAdmin):
    list_display = (
        "id",
        "patient",
    )
    list_select_related = ("care", "care__patient")
    list_filter = ("care__patient",)

    def patient(self, obj):
        return obj.care.patient

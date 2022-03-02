from common.admin import BaseHistoryAdmin
from django.contrib import admin
from ipharm.models.patient_informations import PatientInformation


@admin.register(PatientInformation)
class PatientInformationAdmin(BaseHistoryAdmin):
    list_display = (
        "id",
        "patient",
    )
    list_select_related = ("care", "care__patient")
    list_filter = ("care__patient",)

    def patient(self, obj):
        return obj.care.patient

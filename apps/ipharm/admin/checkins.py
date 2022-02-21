from common.admin import BaseHistoryAdmin
from django.contrib import admin

from .. import models


@admin.register(models.CheckIn)
class CheckInAdmin(BaseHistoryAdmin):
    list_display = ("id", "patient", "medical_procedure", "created_at", "updated_at")
    list_select_related = ("care", "care__patient")
    list_filter = ("care__patient__insurance_company", "medical_procedure")
    search_fields = ("care__patient__birth_number", "care__patient__last_name")
    autocomplete_fields = (
        "drugs",
        "high_interaction_potential_drugs",
        "diagnoses",
        "diagnoses_drugs",
        "narrow_therapeutic_window_drugs",
    )

    def patient(self, obj):
        return obj.care.patient

from common.admin import BaseHistoryAdmin
from django.contrib import admin

from .. import models


@admin.register(models.CheckIn)
class CheckInAdmin(BaseHistoryAdmin):
    list_display = ("id", "patient")
    list_select_related = ("care", "care__patient")
    list_filter = ("care__patient",)
    autocomplete_fields = (
        "drugs",
        "high_interaction_potential_drugs",
        "narrow_therapeutic_window_drugs",
    )

    def patient(self, obj):
        return obj.care.patient

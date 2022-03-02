from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.pharmacological_evaluations import PharmacologicalEvaluation


@admin.register(PharmacologicalEvaluation)
class PharmacologicalEvaluationAdmin(BaseHistoryAdmin):
    list_display = (
        "id",
        "patient",
    )
    list_select_related = ("care", "care__patient")
    list_filter = ("care__patient",)
    autocomplete_fields = ("tags",)

    def patient(self, obj):
        return obj.care.patient

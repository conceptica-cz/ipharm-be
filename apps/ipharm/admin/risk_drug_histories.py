from common.admin import BaseHistoryAdmin
from django.contrib import admin

from .. import models
from ..models.risk_drug_histories import RiskDrugHistory, RiskDrugHistoryComment


class RiskDrugHistoryCommentInline(admin.TabularInline):
    model = RiskDrugHistoryComment
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RiskDrugHistory)
class RiskDrugHistoryAdmin(BaseHistoryAdmin):
    list_display = (
        "id",
        "patient",
    )
    list_select_related = ("care", "care__patient")
    list_filter = ("care__patient",)
    autocomplete_fields = ("risk_drugs", "tags", "risk_diagnoses")
    inlines = (RiskDrugHistoryCommentInline,)

    def patient(self, obj):
        return obj.care.patient

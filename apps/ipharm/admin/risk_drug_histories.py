from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.risk_drug_histories import (
    RiskDrugHistory,
    RiskDrugHistory_tags,
    RiskDrugHistoryComment,
    RiskDrugHistoryDiagnosis,
    RiskDrugHistoryDiagnosisDrug,
)


class RiskDrugHistory_tagsInline(admin.TabularInline):
    model = RiskDrugHistory_tags
    extra = 0
    exclude = ["is_deleted"]
    autocomplete_fields = ["tag"]

    def has_delete_permission(self, request, obj=None):
        return False


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
    search_fields = ("care__patient__birth_number", "care__patient__last_name")
    inlines = (
        RiskDrugHistory_tagsInline,
        RiskDrugHistoryCommentInline,
    )

    def patient(self, obj):
        return obj.care.patient


class RiskDrugHistoryDiagnosisDrugInline(admin.TabularInline):
    model = RiskDrugHistoryDiagnosisDrug
    extra = 0
    exclude = ["is_deleted"]
    autocomplete_fields = ["drug"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RiskDrugHistoryDiagnosis)
class RiskDrugHistoryDiagnosisAdmin(BaseHistoryAdmin):
    list_display = ("id", "risk_drug_history", "diagnosis", "created_at", "updated_at")
    list_select_related = ("risk_drug_history", "diagnosis")
    autocomplete_fields = ["risk_drug_history", "diagnosis"]

    inlines = [RiskDrugHistoryDiagnosisDrugInline]

from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.risk_drug_histories import (
    RiskDrugHistory,
    RiskDrugHistory_risk_diagnoses,
    RiskDrugHistory_risk_drugs,
    RiskDrugHistory_tags,
    RiskDrugHistoryComment,
)


class RiskDrugHistory_risk_drugsInline(admin.TabularInline):
    model = RiskDrugHistory_risk_drugs
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


class RiskDrugHistory_risk_diagnosesInline(admin.TabularInline):
    model = RiskDrugHistory_risk_diagnoses
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


class RiskDrugHistory_tagsInline(admin.TabularInline):
    model = RiskDrugHistory_tags
    extra = 0
    exclude = ["is_deleted"]

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
    inlines = (
        RiskDrugHistory_risk_drugsInline,
        RiskDrugHistory_risk_diagnosesInline,
        RiskDrugHistory_tagsInline,
        RiskDrugHistoryCommentInline,
    )

    def patient(self, obj):
        return obj.care.patient

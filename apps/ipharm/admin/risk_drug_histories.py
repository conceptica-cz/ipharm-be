from common.admin import BaseHistoryAdmin
from django.contrib import admin

from .. import models


class RiskDrugHistoryCommentInline(admin.TabularInline):
    model = models.RiskDrugHistoryComment
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.RiskDrugHistory)
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

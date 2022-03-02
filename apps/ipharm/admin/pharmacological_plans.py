from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)


class PharmacologicalPlanCommentInline(admin.TabularInline):
    model = PharmacologicalPlanComment
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PharmacologicalPlan)
class PharmacologicalPlanAdmin(BaseHistoryAdmin):
    list_display = (
        "id",
        "patient",
    )
    list_select_related = ("care", "care__patient")
    list_filter = ("care__patient",)
    autocomplete_fields = ("tags",)
    inlines = (PharmacologicalPlanCommentInline,)

    def patient(self, obj):
        return obj.care.patient

from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.pharmacological_evaluations import (
    PharmacologicalEvaluation,
    PharmacologicalEvaluation_tags,
    PharmacologicalEvaluationComment,
)


class PharmacologicalEvaluationCommentInline(admin.TabularInline):
    model = PharmacologicalEvaluationComment
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


class PharmacologicalEvaluation_tagsInline(admin.TabularInline):
    model = PharmacologicalEvaluation_tags
    extra = 0
    exclude = ["is_deleted"]
    autocomplete_fields = ["tag"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PharmacologicalEvaluation)
class PharmacologicalEvaluationAdmin(BaseHistoryAdmin):
    list_display = (
        "id",
        "patient",
    )
    list_select_related = ("care", "care__patient")
    list_filter = (
        "deployment",
        "deployment_initial_diagnosis",
        "deployment_during_diagnosis",
        "deployment_ft_approach",
        "discontinuation",
        "discontinuation_contradiction",
        "discontinuation_adverse_effect",
        "discontinuation_adverse_effect_risk",
        "discontinuation_missing_indication",
        "discontinuation_allergies",
        "discontinuation_drug_interaction",
        "discontinuation_duplicity",
        "discontinuation_drug_interaction",
        "discontinuation_renal_insufficiency",
        "discontinuation_hepatic_insufficiency",
        "discontinuation_medical_intervention",
        "discontinuation_underdosage",
        "discontinuation_underdosage_risk",
        "discontinuation_overdosage",
        "discontinuation_overdosage_risk",
    )
    inlines = (
        PharmacologicalEvaluationCommentInline,
        PharmacologicalEvaluation_tagsInline,
    )
    autocomplete_fields = ["drug"]

    def patient(self, obj):
        return obj.care.patient

from common.admin import BaseHistoryAdmin
from django.contrib import admin
from ipharm.models import checkins


class CheckIn_drugsInline(admin.TabularInline):
    model = checkins.CheckIn_drugs
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


class CheckIn_high_interaction_potential_drugsInline(admin.TabularInline):
    model = checkins.CheckIn_high_interaction_potential_drugs
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


class CheckIn_diagnosesInline(admin.TabularInline):
    model = checkins.CheckIn_diagnoses
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


class CheckIn_diagnoses_drugsInline(admin.TabularInline):
    model = checkins.CheckIn_diagnoses_drugs
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


class CheckIn_narrow_therapeutic_window_drugsInline(admin.TabularInline):
    model = checkins.CheckIn_narrow_therapeutic_window_drugs
    extra = 0
    exclude = ["is_deleted"]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(checkins.CheckIn)
class CheckInAdmin(BaseHistoryAdmin):
    list_display = ("id", "patient", "medical_procedure", "created_at", "updated_at")
    list_select_related = ("care", "care__patient")
    list_filter = ("care__patient__insurance_company", "medical_procedure")
    search_fields = ("care__patient__birth_number", "care__patient__last_name")

    inlines = [
        CheckIn_drugsInline,
        CheckIn_high_interaction_potential_drugsInline,
        CheckIn_diagnosesInline,
        CheckIn_diagnoses_drugsInline,
        CheckIn_narrow_therapeutic_window_drugsInline,
    ]

    def patient(self, obj):
        return obj.care.patient

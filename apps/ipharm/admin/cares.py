from common.admin import BaseHistoryAdmin
from django.contrib import admin

from .. import models


@admin.register(models.Drug)
class DrugAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class CheckInline(admin.StackedInline):
    model = models.CheckIn
    autocomplete_fields = (
        "drugs",
        "high_interaction_potential_drugs",
        "narrow_therapeutic_window_drugs",
    )

    def get_exclude(self, request, obj=None):
        default_exclude = ["is_deleted"]
        if self.exclude:
            return list(self.exclude) + default_exclude
        else:
            return default_exclude

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Care)
class CareAdmin(BaseHistoryAdmin):
    list_display = ["pk", "care_type", "patient", "is_active"]
    autocomplete_fields = (
        "main_diagnosis",
        "diagnoses",
    )
    exclude = ["dekurzes"]
    inlines = [CheckInline]

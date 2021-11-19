from common.admin import BaseHistoryAdmin
from django.contrib import admin

from .. import models


class CareDiagnosisInline(admin.TabularInline):
    model = models.CareDiagnosis
    extra = 1


@admin.register(models.Care)
class CareAdmin(BaseHistoryAdmin):
    list_display = ["pk", "care_type", "patient", "is_active"]
    inlines = [CareDiagnosisInline]

from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.MedicalFacility)
class MedicalFacilityAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "facility_id",
        "code",
        "name",
    ]
    search_fields = [
        "facility_id",
        "code",
        "name",
    ]

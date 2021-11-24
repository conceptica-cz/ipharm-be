from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.AdverseEffect)
class AdverseEffectAdmin(BaseHistoryAdmin):
    list_display = [
        "name",
    ]

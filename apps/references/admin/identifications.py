from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.Identification)
class IdentificationAdmin(BaseHistoryAdmin):
    list_display = [
        "name",
        "identifier",
    ]

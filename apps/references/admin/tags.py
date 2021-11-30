from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.Tag)
class TagAdmin(BaseHistoryAdmin):
    list_display = [
        "name",
    ]
    search_fields = ["name"]

from common.admin import BaseHistoryAdmin
from django.contrib import admin
from references import models


@admin.register(models.Person)
class PersonAdmin(BaseHistoryAdmin):
    list_display = [
        "pk",
        "person_number",
        "name",
        "f_title",
        "l_title",
    ]
    search_fields = ["person_number", "name"]

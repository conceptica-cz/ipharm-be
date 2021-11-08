from django.contrib import admin
from references import models
from simple_history.admin import SimpleHistoryAdmin


@admin.register(models.InsuranceCompany)
class InsuranceCompanyAdmin(SimpleHistoryAdmin):
    list_display = [
        "pk",
        "code",
        "name",
    ]
    search_fields = [
        "code",
        "name",
    ]

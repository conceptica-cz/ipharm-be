from django.contrib import admin

# Register your models here.
from reports import models

# @admin.register(models.ReportFile)
# class ReportFileAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "file", "created_at")


@admin.register(models.InsuranceReport)
class InsuranceReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "insurance_company",
        "year",
        "month",
        "created_at",
        "updated_at",
    )

    list_filter = ("insurance_company", "year", "month")

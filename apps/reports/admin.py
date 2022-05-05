# Register your models here.
from common.admin import BaseHistoryAdmin
from django.contrib import admin
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


@admin.register(models.GenericReportType)
class GenericReportTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "file_name", "formats", "order")
    actions = ["generate"]

    @admin.action(description="Generate report")
    def generate(self, request, queryset):
        for report_type in queryset:
            report_type.generate_report()


@admin.register(models.GenericReportFile)
class GenericReportFileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "report_type",
        "report_format",
        "time_range",
        "year",
        "month",
        "date_from",
        "date_to",
        "created_at",
    )

    list_filter = ("report_type",)


@admin.register(models.ReportVariable)
class ReportVariableAdmin(BaseHistoryAdmin):
    list_display = (
        "report_type",
        "name",
        "description",
        "variable_type",
        "value",
        "order",
    )
    list_filter = ("report_type",)

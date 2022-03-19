from django.conf import settings
from django.core.management.base import BaseCommand
from reports.models import GenericReportType, ReportVariable


class Command(BaseCommand):
    help = "Populate database with reports"

    def handle(self, *args, **options):
        print("Creating. Please wait...")
        for report_name, report_data in settings.GENERIC_REPORTS.items():
            report_type, created = GenericReportType.objects.update_or_create(
                name=report_name,
                defaults={
                    "description": report_data["description"],
                    "file_name": report_data["file_name"],
                    "order": report_data["order"],
                    "frequency": report_data["frequency"],
                    "formats": list(report_data["templates"].keys()),
                },
            )
            if created:
                print(f"Created report type: {report_name}")
            for variable in report_data["variables"]:
                _, created = ReportVariable.objects.update_or_create(
                    report_type=report_type,
                    name=variable["name"],
                    defaults={
                        "description": variable["description"],
                        "variable_type": variable["variable_type"],
                        "value": variable["value"],
                        "order": variable["order"],
                    },
                )
                if created:
                    print(f"Created variable: {variable['name']}")

        print("Report was created.")

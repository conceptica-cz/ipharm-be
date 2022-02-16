from django.conf import settings
from django.core.management.base import BaseCommand
from reports.models import GenericReportType


class Command(BaseCommand):
    help = "Populate database with reports"

    def handle(self, *args, **options):
        print("Creating. Please wait...")
        for report_name, report_data in settings.GENERIC_REPORTS.items():
            GenericReportType.objects.update_or_create(
                name=report_name,
                defaults={
                    "description": report_data["description"],
                    "file_name": report_data["file_name"],
                    "order": report_data["order"],
                    "frequency": report_data["frequency"],
                    "formats": list(report_data["templates"].keys()),
                },
            )

        print("Report was created.")

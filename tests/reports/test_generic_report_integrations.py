from pathlib import Path
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.utils import timezone
from reports.models import GenericReportFile

from factories.reports import GenericReportTypeFactory


def test_data_loader(**kwargs):
    return {"test": "test", "year": kwargs.get("year", 2000)}


GENERIC_REPORTS = {
    "monthly_report": {
        "description": "",
        "file_name": "monthly_report",
        "frequency": "monthly",
        "data_loader": "tests.reports.test_generic_report_integrations.test_data_loader",
        "templates": {
            "txt": "test.html",
        },
        "order": 1,
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(__file__).resolve().parent],
        "APP_DIRS": True,
        "OPTIONS": {},
    },
]


@patch("reports.models.timezone.now")
class GenericReportTest(TestCase):
    @override_settings(GENERIC_REPORTS=GENERIC_REPORTS, TEMPLATES=TEMPLATES)
    def test_new_report(self, mocked_now):
        mocked_now.return_value = timezone.datetime(2020, 1, 1, tzinfo=timezone.utc)
        generic_report_type = GenericReportTypeFactory(
            name="monthly_report",
            file_name="test_report",
            formats=["txt"],
            frequency="monthly",
        )

        generic_report_file = generic_report_type.generate_report(report_format="txt")

        self.assertEqual(GenericReportFile.objects.count(), 1)

        self.assertEqual(generic_report_file.year, 2020)
        self.assertEqual(generic_report_file.month, 1)
        self.assertEqual(generic_report_file.report_format, "txt")
        self.assertEqual(
            generic_report_file.file.name, "reports/test_report_2020_01.txt"
        )
        self.assertEqual(generic_report_file.file.read(), b"test 2020")

    @override_settings(GENERIC_REPORTS=GENERIC_REPORTS, TEMPLATES=TEMPLATES)
    def test_update_report(self, mocked_now):
        mocked_now.return_value = timezone.datetime(2020, 1, 1, tzinfo=timezone.utc)
        generic_report_type = GenericReportTypeFactory(
            name="monthly_report",
            file_name="test_report",
            formats=["txt"],
            frequency="monthly",
        )

        generic_report_type.generate_report(report_format="txt")
        generic_report_file = generic_report_type.generate_report(report_format="txt")

        self.assertEqual(GenericReportFile.objects.count(), 1)

        self.assertEqual(generic_report_file.year, 2020)
        self.assertEqual(generic_report_file.month, 1)
        self.assertEqual(generic_report_file.report_format, "txt")
        self.assertEqual(
            generic_report_file.file.name, "reports/test_report_2020_01.txt"
        )
        self.assertEqual(generic_report_file.file.read(), b"test 2020")

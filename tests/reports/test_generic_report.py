from pathlib import Path
from unittest import TestCase

from django.test import override_settings
from reports.generic_report import GenericReport, GenericReportFactory

from factories.reports import GenericReportTypeFactory


def test_data_loader(**kwargs):
    return {"test": "test", "year": kwargs.get("year", "2020")}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [Path(__file__).resolve().parent],
        "APP_DIRS": True,
        "OPTIONS": {},
    },
]


class TestGenericReport(TestCase):
    @override_settings(TEMPLATES=TEMPLATES)
    def test_generic_report(self):
        generic_report = GenericReport(
            data_loader=test_data_loader,
            template="test.html",
            report_format="txt",
            year=2021,
        )

        content = generic_report.render()

        self.assertEqual(content, "test 2021")


GENERIC_REPORTS = {
    "monthly_report": {
        "description": "",
        "file_name": "monthly_report",
        "frequency": "monthly",
        "data_loader": "tests.reports.test_generic_report.test_data_loader",
        "templates": {
            "txt": "test.html",
        },
        "order": 1,
    }
}


class TestGenericReportFactory(TestCase):
    @override_settings(GENERIC_REPORTS=GENERIC_REPORTS)
    def test_generic_report_factory(self):
        report_type = GenericReportTypeFactory(name="monthly_report")

        generic_report_factory = GenericReportFactory()
        generic_report = generic_report_factory.create(
            report_type=report_type, report_format="txt"
        )

        self.assertEqual(generic_report.template, "test.html")
        self.assertEqual(generic_report.data_loader, test_data_loader)
        self.assertEqual(generic_report.report_format, "txt")

from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from reports.models import GenericReportFile, ReportVariable

from factories.reports import GenericReportFileFactory, ReportVariableFactory


class TestReportVariableManager(TestCase):
    def test_as_dict(self):
        ReportVariableFactory(
            name="var_1",
            description="var_1 description",
            variable_type="str",
            value="some text",
        )
        ReportVariableFactory(
            name="var_2",
            description="var_2 description",
            variable_type="int",
            value="42",
        )
        ReportVariableFactory(
            name="var_3",
            description="var_3 description",
            variable_type="bool",
            value="True",
        )
        variables = ReportVariable.objects.as_dict()

        self.assertEqual(variables["var_1"], "some text")
        self.assertEqual(variables["var_2"], 42)
        self.assertEqual(variables["var_3"], True)


class GenericReportFileQuerySetTest(TestCase):
    @patch("reports.managers.timezone.now")
    def test_old_files(self, mock_now):
        mock_now.return_value = timezone.datetime(2020, 1, 3, 0, 0, 0)
        old_file_1 = GenericReportFileFactory()
        old_file_2 = GenericReportFileFactory()
        mock_now.return_value = timezone.datetime(2020, 1, 4, 1, 0, 0)
        new_file_1 = GenericReportFileFactory()
        new_file_2 = GenericReportFileFactory()
        mock_now.return_value = timezone.datetime(2020, 1, 5, 0, 0, 0)

        report_files = GenericReportFile.objects.old_files()

        self.assertQuerysetEqual(
            report_files,
            [old_file_1, old_file_2],
            transform=lambda x: x,
            ordered=False,
        )

    @patch("reports.managers.timezone.now")
    def test_delete_old_files(self, mock_now):
        mock_now.return_value = timezone.datetime(2020, 1, 3, 0, 0, 0)
        old_file_1 = GenericReportFileFactory()
        old_file_2 = GenericReportFileFactory()
        mock_now.return_value = timezone.datetime(2020, 1, 4, 1, 0, 0)
        new_file_1 = GenericReportFileFactory()
        new_file_2 = GenericReportFileFactory()
        mock_now.return_value = timezone.datetime(2020, 1, 5, 0, 0, 0)

        GenericReportFile.objects.delete_old_files()

        report_files = GenericReportFile.objects.all()

        self.assertQuerysetEqual(
            report_files,
            [new_file_1, new_file_2],
            transform=lambda x: x,
            ordered=False,
        )

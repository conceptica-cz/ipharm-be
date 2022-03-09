from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from reports.uzis import uzis_loader

from factories.ipharm import CheckInFactory
from factories.references import DepartmentFactory, IdentificationFactory
from factories.reports import GenericReportTypeFactory, ReportVariableFactory


class TestUzisLoader(TestCase):
    def setUp(self) -> None:
        self.identification = IdentificationFactory(for_insurance=True)
        self.department = DepartmentFactory(for_insurance=True)

    def test_uzis_loader(self):
        report_type = GenericReportTypeFactory()
        ReportVariableFactory(
            report_type=report_type,
            name="string_variable",
            description="String variable",
            variable_type="str",
            value="text",
        )
        ReportVariableFactory(
            report_type=report_type,
            name="integer_variable",
            description="Integer variable",
            variable_type="int",
            value="42",
        )
        kwargs = {"year": 2020}

        data = uzis_loader(**kwargs)

        self.assertEqual(data["variables"]["string_variable"], "text")
        self.assertEqual(data["variables"]["integer_variable"], 42)

    @patch("django.utils.timezone.now")
    def test_uzis_medical_procedures(self, mocked_now):
        now_2019 = timezone.datetime(2019, 2, 1, tzinfo=timezone.utc)
        now_2020 = timezone.datetime(2020, 3, 1, tzinfo=timezone.utc)
        mocked_now.return_value = now_2020
        CheckInFactory(
            care__patient__insurance_number=1111111111,
            risk_level="2",
        )
        CheckInFactory(
            care__patient__insurance_number=2222222222,
            risk_level="2",
        )
        # that checkin has medical_procedure=None
        CheckInFactory(
            care__patient__insurance_number=3333333333,
            risk_level="1",
            patient_condition_change=False,
        )
        mocked_now.return_value = now_2019
        CheckInFactory(
            care__patient__insurance_number=4444444444,
            risk_level="2",
        )

        kwargs = {"year": 2020}

        data = uzis_loader(**kwargs)

        self.assertEqual(data["medical_procedures"]["05751"], 2)

    def test_uzis_header(self):

        kwargs = {"year": 2020}

        data = uzis_loader(**kwargs)

        self.assertEqual(data["header"]["year"], 2020)

        self.assertEqual(data["header"]["name"], self.identification.name)
        self.assertEqual(data["header"]["address"], self.identification.address)
        self.assertEqual(data["header"]["zip"], self.identification.zip)
        self.assertEqual(data["header"]["city"], self.identification.city)
        self.assertEqual(data["header"]["ico"], self.identification.ico)

        self.assertEqual(data["header"]["department_name"], self.department.description)

    @patch("reports.uzis.timezone.now")
    def test_uzis_signature(self, mocked_now):
        now = timezone.datetime(2021, 3, 15, tzinfo=timezone.utc)
        mocked_now.return_value = now
        kwargs = {"year": 2020}

        data = uzis_loader(**kwargs)

        self.assertEqual(data["signature"]["date"], "15.3.2021")

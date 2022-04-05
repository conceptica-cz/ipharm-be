from datetime import date
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from reports.generic_reports import statistical_reports

from factories.ipharm import CheckInFactory
from factories.references import ClinicFactory, DepartmentFactory


class RiskLevelsLoadersTest(TestCase):
    @patch("django.utils.timezone.now")
    def setUp(self, mocked_now):
        now_2019_12 = timezone.datetime(2019, 12, 2, tzinfo=timezone.utc)
        now_2020_01 = timezone.datetime(2020, 1, 2, tzinfo=timezone.utc)
        now_2020_02 = timezone.datetime(2020, 2, 2, tzinfo=timezone.utc)
        mocked_now.return_value = now_2019_12

        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()

        self.department_1 = DepartmentFactory(clinic=self.clinic_1)
        self.department_2 = DepartmentFactory(clinic=self.clinic_1)
        self.department_3 = DepartmentFactory(clinic=self.clinic_2)

        CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_1,
            care__department=self.department_1,
        )
        CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_1,
            care__department=self.department_2,
        )
        CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )
        CheckInFactory(
            risk_level=2,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )
        CheckInFactory(
            risk_level=2,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )
        CheckInFactory(
            risk_level=3,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )

        mocked_now.return_value = now_2020_01
        CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )
        CheckInFactory(
            risk_level=2,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )
        CheckInFactory(
            risk_level=3,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )

        mocked_now.return_value = now_2020_02
        CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_1,
            care__department=self.department_2,
        )
        CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )
        CheckInFactory(
            risk_level=2,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )
        CheckInFactory(
            risk_level=3,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )

    def test_loader__all(self):
        data = statistical_reports.risk_level_loader(time_range="custom")

        self.assertEqual(data["hospital_risk_level_1"], 6)
        self.assertEqual(data["hospital_risk_level_2"], 4)
        self.assertEqual(data["hospital_risk_level_3"], 3)

    def test_loader__2019(self):
        data = statistical_reports.risk_level_loader(time_range="year", year=2019)

        self.assertEqual(data["hospital_risk_level_1"], 3)

    def test_loader__2020_02(self):
        data = statistical_reports.risk_level_loader(
            time_range="month", year=2020, month=2
        )

        self.assertEqual(data["hospital_risk_level_1"], 2)

    def test_loader__from_2020_01_01_to_2020_02_01(self):
        data = statistical_reports.risk_level_loader(
            time_range="custom",
            date_from=date(2020, 1, 1),
            date_to=date(2020, 2, 1),
        )

        self.assertEqual(data["hospital_risk_level_1"], 1)

    def test_loader__from_2020_01_01(self):
        data = statistical_reports.risk_level_loader(
            time_range="custom",
            date_from=date(2020, 1, 1),
        )

        self.assertEqual(data["hospital_risk_level_1"], 3)

    def test_loader__department_2(self):
        data = statistical_reports.risk_level_loader(
            time_range="custom", filters={"department": self.department_2.pk}
        )

        self.assertEqual(data["hospital_risk_level_1"], 2)

    def test_loader__clinic_1_2019(self):
        data = statistical_reports.risk_level_loader(
            time_range="year", year=2019, filters={"clinic": self.clinic_1.pk}
        )

        self.assertEqual(data["hospital_risk_level_1"], 2)

from datetime import date
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone
from reports.generic_reports import statistical_reports

from factories.ipharm import (
    CheckInFactory,
    PharmacologicalEvaluationFactory,
    PharmacologicalPlanCommentFactory,
    PharmacologicalPlanFactory,
    RiskDrugHistoryFactory,
)
from factories.references import (
    ClinicFactory,
    DepartmentFactory,
    DrugFactory,
    TagFactory,
)


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

        check_in = CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_1,
            care__department=self.department_1,
        )

        plan = PharmacologicalPlanFactory(care=check_in.care)
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="comment"
        )
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="verification", verify=True
        )

        check_in = CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_1,
            care__department=self.department_2,
        )

        PharmacologicalPlanFactory(care=check_in.care)

        CheckInFactory(
            risk_level=1,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )
        check_in = CheckInFactory(
            risk_level=2,
            care__care_type="hospitalization",
            care__clinic=self.clinic_2,
            care__department=self.department_3,
        )

        plan = PharmacologicalPlanFactory(care=check_in.care)
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="verification", verify=True
        )
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=plan, comment_type="verification", verify=False
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
            care__care_type="ambulation",
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
        self.assertEqual(data["hospital_risk_level_3"], 2)
        self.assertEqual(data["ambulance_risk_level_3"], 1)

        self.assertEqual(data["pharmacological_plan_hospital_risk_level_1"], 2)
        self.assertEqual(data["pharmacological_plan_hospital_risk_level_2"], 1)

        self.assertEqual(
            data["pharmacological_plan_verification_hospital_risk_level_1"], 1
        )
        self.assertEqual(
            data["pharmacological_plan_verification_hospital_risk_level_2"], 2
        )

    def test_loader__patient_type_hospitalization(self):
        data = statistical_reports.risk_level_loader(
            time_range="custom", filters={"care_type": ("hospitalization",)}
        )

        self.assertEqual(data["hospital_risk_level_1"], 6)
        self.assertEqual(data["hospital_risk_level_2"], 4)
        self.assertEqual(data["hospital_risk_level_3"], 2)
        self.assertEqual(data["ambulance_risk_level_3"], 0)

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


class TestTagsLoader(TestCase):
    @patch("django.utils.timezone.now")
    def setUp(self, mocked_now):
        now_2019_12 = timezone.datetime(2019, 12, 2, tzinfo=timezone.utc)
        now_2020_01 = timezone.datetime(2020, 1, 2, tzinfo=timezone.utc)

        mocked_now.return_value = now_2019_12

        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()

        self.tag_1 = TagFactory(name="tag_1")
        self.tag_2 = TagFactory(name="tag_2")
        self.tag_3 = TagFactory(name="tag_3")

        pe = PharmacologicalEvaluationFactory(care__clinic=self.clinic_1)
        pe.tags.set([self.tag_1, self.tag_2])

        mocked_now.return_value = now_2020_01

        pe = PharmacologicalEvaluationFactory(care__clinic=self.clinic_2)
        pe.tags.set([self.tag_1])

        pp = PharmacologicalPlanFactory(care__clinic=self.clinic_1)
        pp.tags.set([self.tag_1])

        pp = RiskDrugHistoryFactory(care__clinic=self.clinic_1)
        pp.tags.set([self.tag_2])

    def test_loader__all(self):
        data = statistical_reports.tags_loader(time_range="custom")

        tags = data["tags"]

        tag_1 = tags.get(name="tag_1")
        self.assertEqual(tag_1.evaluation_count, 2)
        self.assertEqual(tag_1.plan_count, 1)
        self.assertEqual(tag_1.history_count, 0)
        self.assertEqual(tag_1.total_count, 3)

        tag_2 = tags.get(name="tag_2")
        self.assertEqual(tag_2.evaluation_count, 1)
        self.assertEqual(tag_2.plan_count, 0)
        self.assertEqual(tag_2.history_count, 1)
        self.assertEqual(tag_2.total_count, 2)

    def test_loader__clinic_1(self):
        data = statistical_reports.tags_loader(
            time_range="custom", filters={"clinic": self.clinic_1.pk}
        )

        tags = data["tags"]

        self.assertEqual(len(tags), 2)

        tag_1 = tags.get(name="tag_1")
        self.assertEqual(tag_1.evaluation_count, 1)

        tag_2 = tags.get(name="tag_2")
        self.assertEqual(tag_2.evaluation_count, 1)

    def test_loader__year_2020(self):
        data = statistical_reports.tags_loader(time_range="year", year=2020)

        tags = data["tags"]

        self.assertEqual(len(tags), 2)

        tag_1 = tags.get(name="tag_1")
        self.assertEqual(tag_1.evaluation_count, 1)


class TestEvaluationDrugsLoader(TestCase):
    @patch("django.utils.timezone.now")
    def setUp(self, mocked_now):
        now_2019_12 = timezone.datetime(2019, 12, 2, tzinfo=timezone.utc)
        now_2020_01 = timezone.datetime(2020, 1, 2, tzinfo=timezone.utc)

        mocked_now.return_value = now_2019_12

        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()

        self.drug_2 = DrugFactory(name="drug_2")
        self.drug_1 = DrugFactory(name="drug_1")
        self.drug_3 = DrugFactory(name="drug_3")

        PharmacologicalEvaluationFactory(
            drug=self.drug_1,
            care__clinic=self.clinic_1,
            deployment=True,
            deployment_initial_diagnosis=False,
            continuation=False,
        )
        PharmacologicalEvaluationFactory(
            drug=self.drug_1,
            care__clinic=self.clinic_2,
            deployment=True,
            deployment_initial_diagnosis=True,
            continuation=False,
        )

        PharmacologicalEvaluationFactory(
            drug=self.drug_2,
            care__clinic=self.clinic_2,
            deployment=False,
            deployment_initial_diagnosis=False,
            continuation=True,
        )

        mocked_now.return_value = now_2020_01

        PharmacologicalEvaluationFactory(
            drug=self.drug_1,
            care__clinic=self.clinic_1,
            deployment=True,
            deployment_initial_diagnosis=False,
            continuation=False,
        )

    def test_loader__all(self):
        data = statistical_reports.evaluation_drugs_loader(time_range="custom")

        drugs = data["drugs"]

        self.assertEqual(len(drugs), 2)

        self.assertEqual(drugs[0].name, "drug_1")
        self.assertEqual(drugs[1].name, "drug_2")

        counts = data["counts"]

        self.assertEqual(counts["deployment_count"]["drug_1"], 3)
        self.assertEqual(counts["deployment_count"]["drug_2"], 0)
        self.assertEqual(counts["deployment_initial_diagnosis_count"]["drug_1"], 1)
        self.assertEqual(counts["deployment_initial_diagnosis_count"]["drug_2"], 0)
        self.assertEqual(counts["continuation_count"]["drug_1"], 0)
        self.assertEqual(counts["continuation_count"]["drug_2"], 1)

    def test_loader__clinic_1(self):
        data = statistical_reports.evaluation_drugs_loader(
            time_range="custom", filters={"clinic": self.clinic_1.pk}
        )

        drugs = data["drugs"]

        self.assertEqual(len(drugs), 1)

        self.assertEqual(drugs[0].name, "drug_1")

        counts = data["counts"]

        self.assertEqual(counts["deployment_count"]["drug_1"], 2)
        self.assertEqual(counts["deployment_initial_diagnosis_count"]["drug_1"], 0)
        self.assertEqual(counts["continuation_count"]["drug_1"], 0)

    def test_loader__year_2020(self):
        data = statistical_reports.evaluation_drugs_loader(time_range="year", year=2020)

        drugs = data["drugs"]

        self.assertEqual(len(drugs), 1)

        self.assertEqual(drugs[0].name, "drug_1")

        counts = data["counts"]

        self.assertEqual(counts["deployment_count"]["drug_1"], 1)
        self.assertEqual(counts["deployment_initial_diagnosis_count"]["drug_1"], 0)
        self.assertEqual(counts["continuation_count"]["drug_1"], 0)

    def test_xlsx_transformer(self):
        data = statistical_reports.evaluation_drugs_loader(time_range="custom")
        xlsx_data = statistical_reports.evaluation_drugs_xlsx_data_transformer(data)

        header = xlsx_data["data"][0]
        drugs = xlsx_data["data"][1]
        deployment_count = xlsx_data["data"][2]

        self.assertEqual(len(header), 3)
        self.assertEqual(len(xlsx_data["widths"]), 3)
        self.assertEqual(xlsx_data["merges"], [(0, 0, 0, 2)])

        self.assertEqual(drugs, ["", "drug_1", "drug_2"])

        self.assertEqual(deployment_count[0][0], "Nasazení léčiva")
        self.assertEqual(deployment_count[1], 3)
        self.assertEqual(deployment_count[2], 0)


class TestEvaluationGroupsLoader(TestCase):
    @patch("django.utils.timezone.now")
    def setUp(self, mocked_now):
        now_2019_12 = timezone.datetime(2019, 12, 2, tzinfo=timezone.utc)
        now_2020_01 = timezone.datetime(2020, 1, 2, tzinfo=timezone.utc)

        mocked_now.return_value = now_2019_12

        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()

        self.drug_1 = DrugFactory(name="drug_1", atc_group="AA2")
        self.drug_2 = DrugFactory(name="drug_2", atc_group="AA2")
        self.drug_3 = DrugFactory(name="drug_3", atc_group="AA1")
        self.drug_4 = DrugFactory(name="drug_4", atc_group="AB1")

        PharmacologicalEvaluationFactory(
            drug=self.drug_1,
            care__clinic=self.clinic_1,
            deployment=True,
        )
        PharmacologicalEvaluationFactory(
            drug=self.drug_2,
            care__clinic=self.clinic_2,
            deployment=True,
        )

        PharmacologicalEvaluationFactory(
            drug=self.drug_2,
            care__clinic=self.clinic_2,
            deployment=False,
        )
        PharmacologicalEvaluationFactory(
            drug=self.drug_3,
            care__clinic=self.clinic_2,
            deployment=True,
        )
        PharmacologicalEvaluationFactory(
            drug=self.drug_4,
            care__clinic=self.clinic_2,
            deployment=True,
        )

        mocked_now.return_value = now_2020_01

        PharmacologicalEvaluationFactory(
            drug=self.drug_1,
            care__clinic=self.clinic_1,
            deployment=True,
        )

    def test_loader__a_groups(self):
        data = statistical_reports.evaluation_groups_loader(
            time_range="custom", filters={"atc_group_startswith": "A"}
        )

        groups = data["groups"]

        self.assertEqual(len(groups), 3)

        self.assertEqual(groups[0]["atc_group"], "AA1")
        self.assertEqual(groups[1]["atc_group"], "AA2")
        self.assertEqual(groups[2]["atc_group"], "AB1")

        counts = data["counts"]

        self.assertEqual(counts["deployment_count"]["AA1"], 1)
        self.assertEqual(counts["deployment_count"]["AA2"], 3)
        self.assertEqual(counts["deployment_count"]["AB1"], 1)

    def test_loader__aa_groups(self):
        data = statistical_reports.evaluation_groups_loader(
            time_range="custom", filters={"atc_group_startswith": "AA"}
        )

        groups = data["groups"]

        self.assertEqual(len(groups), 2)

        self.assertEqual(groups[0]["atc_group"], "AA1")
        self.assertEqual(groups[1]["atc_group"], "AA2")

        counts = data["counts"]

        self.assertEqual(counts["deployment_count"]["AA1"], 1)
        self.assertEqual(counts["deployment_count"]["AA2"], 3)

from django.urls import reverse
from reports.models import GenericReportFile
from reports.serializers import GenericReportFileSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references import DepartmentFactory, IdentificationFactory
from factories.reports import GenericReportTypeFactory, ReportVariableFactory
from factories.users import UserFactory


class ReportsTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.report_1 = GenericReportTypeFactory()
        self.report_2 = GenericReportTypeFactory()

    def test_get_all_reports(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("report_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], self.report_1.name)
        self.assertEqual(response.data["results"][1]["name"], self.report_2.name)


class ReportVariablesTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.report_1 = GenericReportTypeFactory()
        another_report = GenericReportTypeFactory()
        self.variable_1 = ReportVariableFactory(
            report_type=self.report_1,
            name="variable_1",
            description="variable_1 description",
            variable_type="str",
            value="str_value",
            order=1,
        )
        self.variable_2 = ReportVariableFactory(
            report_type=self.report_1,
            name="variable_2",
            description="variable_2 description",
            variable_type="int",
            value="1",
            order=2,
        )
        self.variable_3 = ReportVariableFactory(
            report_type=another_report,
            name="variable_3",
            description="variable_3 description",
            variable_type="str",
            value="str_value",
            order=1,
        )

    def test_get_all_report_variables(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("report_variable_list", kwargs={"pk": self.report_1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], self.variable_1.name)
        self.assertEqual(response.data["results"][1]["name"], self.variable_2.name)
        self.assertEqual(response.data["results"][0]["value"], self.variable_1.value)
        self.assertEqual(response.data["results"][1]["value"], self.variable_2.value)

    def test_get_variable_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(
                "report_variable_detail",
                kwargs={"pk": self.variable_1.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.variable_1.name)
        self.assertEqual(response.data["value"], self.variable_1.value)

    def test_patch_variable_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse(
                "report_variable_detail",
                kwargs={"pk": self.variable_1.pk},
            ),
            data={"value": "new_value"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.variable_1.refresh_from_db()

        self.assertEqual(self.variable_1.value, "new_value")

    def test_patch_variable_detail__invalid_value(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse(
                "report_variable_detail",
                kwargs={"pk": self.variable_2.pk},
            ),
            data={"value": "not_a_number"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.variable_2.refresh_from_db()

        self.assertEqual(self.variable_2.value, "1")


class GenerateReportTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.report = GenericReportTypeFactory(name="uzis")

    def test_generate(self):
        IdentificationFactory(for_insurance=True)
        DepartmentFactory(for_insurance=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("report_generate", kwargs={"pk": self.report.pk}),
            data={"year": 2020},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(GenericReportFile.objects.count(), 1)

        self.assertEqual(
            response.data,
            GenericReportFileSerializer(
                instance=GenericReportFile.objects.first()
            ).data,
        )

    def test_generate__without_identification(self):
        DepartmentFactory(for_insurance=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("report_generate", kwargs={"pk": self.report.pk}),
            data={"year": 2020},
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data
        )

    def test_generate__without_department(self):
        IdentificationFactory(for_insurance=True)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("report_generate", kwargs={"pk": self.report.pk}),
            data={"year": 2020},
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data
        )

from django.test import TestCase
from reports.models import ReportVariable

from factories.reports import ReportVariableFactory


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

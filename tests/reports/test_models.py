from django.core.exceptions import ValidationError
from django.test import TestCase
from reports.models import ReportVariable

from factories.reports import ReportVariableFactory


class ReportVariableTest(TestCase):
    def test_casted_value(self):
        variable = ReportVariableFactory(
            name="test_variable", value="1", variable_type="int"
        )

        self.assertEqual(variable.casted_value, 1)

    def test_clean_value(self):
        variable = ReportVariable(
            name="test_variable",
            value="not a number",
            variable_type="int",
        )
        with self.assertRaises(ValidationError) as context:
            variable.save()

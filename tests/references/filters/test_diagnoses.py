from django.test import TestCase
from references.filters import DiagnosisFilter

from factories.references import DiagnosisFactory


class DiagnosisFilterTest(TestCase):
    def setUp(self) -> None:
        self.diagnosis_1 = DiagnosisFactory(code="A01")
        self.diagnosis_2 = DiagnosisFactory(code="A02")
        self.diagnosis_3 = DiagnosisFactory(code="E10")
        self.diagnosis_4 = DiagnosisFactory(code="E110")
        self.diagnosis_5 = DiagnosisFactory(code="E12")
        self.diagnosis_6 = DiagnosisFactory(code="E13")
        self.diagnosis_7 = DiagnosisFactory(code="E14")
        self.diagnosis_8 = DiagnosisFactory(code="E15")

    def test_get_codes(self):
        codes = DiagnosisFilter._get_codes()
        self.assertIn("E10", codes)
        self.assertIn("E11", codes)
        self.assertIn("E14", codes)
        self.assertIn("I48", codes)
        self.assertIn("G40", codes)
        self.assertIn("G41", codes)
        self.assertIn("C00", codes)
        self.assertIn("C01", codes)
        self.assertIn("C10", codes)
        self.assertIn("C96", codes)
        self.assertIn("C97", codes)
        self.assertNotIn("C98", codes)
        self.assertIn("G20", codes)
        self.assertIn("G21", codes)

    def test_clinical_pharmacology_filter(self):
        f = DiagnosisFilter(data={"clinical_pharmacology": True})
        queryset = f.qs
        self.assertEqual(queryset.count(), 5)
        self.assertQuerysetEqual(
            queryset,
            [
                self.diagnosis_3,
                self.diagnosis_4,
                self.diagnosis_5,
                self.diagnosis_6,
                self.diagnosis_7,
            ],
            transform=lambda x: x,
            ordered=False,
        )

        f = DiagnosisFilter(data={"clinical_pharmacology": False})
        queryset = f.qs
        self.assertEqual(queryset.count(), 8)

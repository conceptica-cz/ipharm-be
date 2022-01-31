from django.test import TestCase

from factories.ipharm import CheckInFactory


class TestCheckins(TestCase):
    def test_has_insurance_report_is_not_set_for_risk_level_1(self):
        check_in = CheckInFactory(risk_level="1", patient_condition_change=False)
        self.assertEqual(check_in.in_insurance_report, False)

    def test_has_insurance_report_is_set_for_risk_level_2(self):
        check_in = CheckInFactory(risk_level="2", patient_condition_change=False)
        self.assertEqual(check_in.in_insurance_report, True)

    def test_has_insurance_report_is_set_for_risk_level_3(self):
        check_in = CheckInFactory(risk_level="3", patient_condition_change=False)
        self.assertEqual(check_in.in_insurance_report, True)

    def test_has_insurance_report_is_set_if_patient_condition_change(self):
        check_in = CheckInFactory(risk_level="1", patient_condition_change=True)
        self.assertEqual(check_in.in_insurance_report, True)

    def test_it_is_impossible_to_downgrade_has_insurance_report_to_false(self):
        check_in = CheckInFactory(risk_level="1", patient_condition_change=False)
        check_in.risk_level = "2"
        check_in.save()
        self.assertEqual(check_in.in_insurance_report, True)
        check_in.risk_level = "1"
        check_in.patient_condition_change = False
        check_in.save()
        self.assertEqual(check_in.in_insurance_report, True)

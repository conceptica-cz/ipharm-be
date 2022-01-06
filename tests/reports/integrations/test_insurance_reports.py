import functools

from django.test import TestCase
from django.utils import timezone
from reports.insurance_report import check_in_dosage

from factories.ipharm import CareFactory, CheckInFactory, PatientFactory
from factories.references import (
    DepartmentFactory,
    DiagnosisFactory,
    InsuranceCompanyFactory,
    MedicalProcedureFactory,
)


class InsuranceReportTestCase(TestCase):
    def test_insurance_report(self):
        pass


class CheckInDosageTestCase(TestCase):
    def test_check_in_dosage(self):
        insurance_company = InsuranceCompanyFactory(code="123")
        patient = PatientFactory(
            insurance_company=insurance_company, insurance_number="1234567890"
        )
        diagnosis = DiagnosisFactory(code="K00")
        care = CareFactory(
            patient=patient,
            main_diagnosis=diagnosis,
            department__icp="142",
            department__specialization_code="242",
            started_at=timezone.datetime(2019, 1, 10, 0, 0, 0),
        )
        check_in = CheckInFactory(care=care)

        department_for_insurance = DepartmentFactory(
            icp="542", ns="642", specialization_code="742"
        )

        medical_procedure = MedicalProcedureFactory(scores=42)

        dosage = check_in_dosage(
            check_in=check_in,
            department_for_insurance=department_for_insurance,
            medical_procedure=medical_procedure,
        )

        heading = dosage["heading"]
        result = dosage["result"]

        heading_len = len(functools.reduce(lambda s1, s2: s1 + s2, heading.values()))
        self.assertEqual(heading_len, 100)

        result_len = len(functools.reduce(lambda s1, s2: s1 + s2, result.values()))
        self.assertEqual(result_len, 16)

        self.assertEqual(heading["TYP"], "E")
        self.assertEqual(heading["ECID"], "*******")
        self.assertEqual(heading["ESTR"], "0")
        self.assertEqual(heading["EPOC"], "0")
        self.assertEqual(heading["EPOR"], "***")
        self.assertEqual(heading["ECPO"], "123")
        self.assertEqual(heading["ETPP"], "1")
        self.assertEqual(heading["EICO"], "     542")
        self.assertEqual(heading["EVAR"], "   642")
        self.assertEqual(heading["EODB"], "742")
        self.assertEqual(heading["EROD"], "1234567890")
        self.assertEqual(heading["EZDG"], "  K00")
        self.assertEqual(heading["EKO"], " ")
        self.assertEqual(heading["EICZ"], "     142")
        self.assertEqual(heading["ECDZ"], "       ")
        self.assertEqual(heading["EDAT"], "10012019")
        self.assertEqual(heading["ECCEL"], "          ")
        self.assertEqual(heading["ECBOD"], "     42")
        self.assertEqual(heading["EODZ"], "242")
        self.assertEqual(heading["EVARZ"], "      ")
        self.assertEqual(heading["DTYP"], " ")

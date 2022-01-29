import functools

from django.test import TestCase
from django.utils import timezone
from reports import insurance_report
from reports.models import InsuranceReport

from factories.ipharm import CareFactory, CheckInFactory, PatientFactory
from factories.references import (
    DepartmentFactory,
    DiagnosisFactory,
    IdentificationFactory,
    InsuranceCompanyFactory,
    MedicalProcedureFactory,
)
from factories.reports import InsuranceReportFactory


class InsuranceReportTestCase(TestCase):
    def setUp(self) -> None:
        check_in = CheckInFactory(
            care__patient__insurance_number=1111111111,
            care__patient__insurance_company__code=111,
            created_at=timezone.datetime(2019, 2, 12, 0, 0, 0, tzinfo=timezone.utc),
            for_insurance=True,
        )
        CheckInFactory(
            care__patient__insurance_number=2222222222,
            care__patient__insurance_company__code=111,
            created_at=timezone.datetime(2019, 2, 12, 0, 0, 0, tzinfo=timezone.utc),
            for_insurance=True,
        )
        CheckInFactory(
            care__patient__insurance_number=3333333333,
            care__patient__insurance_company__code=111,
            created_at=timezone.datetime(2019, 2, 12, 0, 0, 0, tzinfo=timezone.utc),
            for_insurance=False,
        )
        another_check_in = CheckInFactory(
            care__patient__insurance_number=4444444444,
            care__patient__insurance_company__code=222,
            created_at=timezone.datetime(2019, 2, 12, 0, 0, 0, tzinfo=timezone.utc),
            for_insurance=True,
        )
        CheckInFactory(
            care__patient__insurance_number=5555555555,
            care__patient__insurance_company__code=111,
            created_at=timezone.datetime(2019, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
            for_insurance=True,
        )
        CheckInFactory(
            care__patient__insurance_number=6666666666,
            care__patient__insurance_company__code=111,
            created_at=timezone.datetime(2018, 2, 12, 0, 0, 0, tzinfo=timezone.utc),
            for_insurance=True,
        )

        MedicalProcedureFactory(code="05751", scores=185)
        self.identification = IdentificationFactory(
            identifier="12345678", for_insurance=True
        )
        self.department_for_insurance = DepartmentFactory(
            icp="542", ns="642", specialization_code="742", for_insurance=True
        )
        self.insurance_company = check_in.care.patient.insurance_company
        self.another_insurance_company = another_check_in.care.patient.insurance_company

    def test_get_insurance_report_data(self):
        data = insurance_report.get_insurance_report_data(
            insurance_company=self.insurance_company,
            year=2019,
            month=2,
            start_number=142,
            identification=self.identification,
            department_for_insurance=self.department_for_insurance,
        )

        self.assertEqual(len(data["documents"]), 2)
        self.assertEqual(data["dosage"]["DBODY"], "      370.0")

    def test_generate_insurance_report(self):
        content = insurance_report.generate_insurance_report(
            insurance_company=self.insurance_company,
            year=2019,
            month=2,
            start_number=142,
            identification=self.identification,
            department_for_insurance=self.department_for_insurance,
        )

        report = InsuranceReport.objects.first()
        self.assertEqual(len(report.data["documents"]), 2)
        self.assertIn("1111111111", report.content)
        self.assertEqual(report.documents_number, 2)
        self.assertEqual(report.year, 2019)
        self.assertEqual(report.month, 2)
        self.assertEqual(report.insurance_company, self.insurance_company)

    def test_generate_all_reports__creates_reports_for_current_and_previous_month(self):
        InsuranceReportFactory(
            insurance_company=self.insurance_company,
            year=2018,
            month=12,
            documents_number=2,
        )
        InsuranceReportFactory(
            insurance_company=self.another_insurance_company,
            year=2018,
            month=12,
            documents_number=7,
        )
        insurance_report.generate_all_reports(year=2019, month=2)

        self.assertEqual(InsuranceReport.objects.count(), 5)

    def test_generate_all_reports__updates_already_existing_reports(self):
        InsuranceReportFactory(
            insurance_company=self.insurance_company,
            year=2018,
            month=12,
            documents_number=2,
        )
        InsuranceReportFactory(
            insurance_company=self.another_insurance_company,
            year=2018,
            month=12,
            documents_number=7,
        )
        insurance_report.generate_all_reports(year=2019, month=2)
        insurance_report.generate_all_reports(year=2019, month=2)
        insurance_report.generate_all_reports(year=2019, month=2)

        self.assertEqual(InsuranceReport.objects.count(), 5)


class DosageDataTest(TestCase):
    def test_dosage_data(self):
        insurance_company = InsuranceCompanyFactory(code="111", type="2")
        identification = IdentificationFactory(identifier="12345678")
        documents = [
            {"heading": {"ECBOD": "   42"}},
            {"heading": {"ECBOD": "   42"}},
            {"heading": {"ECBOD": "   42"}},
        ]
        dosage_data = insurance_report.get_dosage_data(
            insurance_company=insurance_company,
            identification=identification,
            year=2020,
            month=2,
            documents=documents,
        )

        self.assertEqual(dosage_data["TYP"], "D")
        self.assertEqual(dosage_data["CHAR"], "P")
        self.assertEqual(dosage_data["DTYP"], "90")
        self.assertEqual(dosage_data["DICO"], "12345678")
        self.assertEqual(dosage_data["DPOB"], "1234")
        self.assertEqual(dosage_data["DROK"], "2020")
        self.assertEqual(dosage_data["DMES"], "02")
        self.assertEqual(dosage_data["DCID"], "    02")
        self.assertEqual(dosage_data["DPOC"], "  3")
        self.assertEqual(dosage_data["DBODY"], "      126.0")
        self.assertEqual(dosage_data["DFIN"], "                  ")
        self.assertEqual(dosage_data["DDPP"], "2")
        self.assertEqual(dosage_data["DVDR1"], "    06:6.2.42")
        self.assertEqual(dosage_data["DVDR2"], "             ")


class CheckInDocumentTest(TestCase):
    def test_check_in_document_data(self):
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
            started_at=timezone.datetime(2019, 1, 10, 0, 0, 0, tzinfo=timezone.utc),
        )
        check_in = CheckInFactory(
            care=care,
            created_at=timezone.datetime(2019, 1, 12, 0, 0, 0, tzinfo=timezone.utc),
        )

        department_for_insurance = DepartmentFactory(
            icp="542", ns="642", specialization_code="742"
        )

        medical_procedure = MedicalProcedureFactory(code="42424", scores=42)

        dosage = insurance_report.get_document_data(
            obj=check_in,
            department_for_insurance=department_for_insurance,
            medical_procedure=medical_procedure,
            document_number=2,
            document_total_number=42,
        )

        heading = dosage["heading"]
        result = dosage["result"]

        heading_len = len(functools.reduce(lambda s1, s2: s1 + s2, heading.values()))
        self.assertEqual(heading_len, 100)

        result_len = len(functools.reduce(lambda s1, s2: s1 + s2, result.values()))
        self.assertEqual(result_len, 16)

        self.assertEqual(heading["TYP"], "E")
        self.assertEqual(heading["ECID"], "     42")
        self.assertEqual(heading["ESTR"], "0")
        self.assertEqual(heading["EPOC"], "0")
        self.assertEqual(heading["EPOR"], "  2")
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

        self.assertEqual(result["TYP"], "V")
        self.assertEqual(result["VDAT"], "12012019")
        self.assertEqual(result["VKOD"], "42424")
        self.assertEqual(result["VPOC"], " ")
        self.assertEqual(result["DTYP"], " ")

import factory

from factories.references import InsuranceCompanyFactory


class InsuranceReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "reports.InsuranceReport"

    insurance_company = factory.SubFactory(InsuranceCompanyFactory)
    documents_number = 10
    year = 2021
    month = 1
    data = {}
    content = ""


class GenericReportTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "reports.GenericReportType"

    name = "Test Report"
    description = "Test Report Description"
    file_name = "test_report"
    formats = ["pdf"]
    frequency = "monthly"
    order = 1


class GenericReportFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "reports.GenericReportFile"

    report_type = factory.SubFactory(GenericReportTypeFactory)
    file = None
    year = 2020
    month = 1
    format = "pdf"

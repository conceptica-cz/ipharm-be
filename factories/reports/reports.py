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
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"report_type_{n}")
    description = factory.Sequence(lambda n: f"report_type_description_{n}")
    file_name = factory.Sequence(lambda n: f"report_type_file_name_{n}")
    time_ranges = ["month"]
    filters = []
    formats = ["txt"]
    order = factory.Sequence(lambda n: n)


class GenericReportFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "reports.GenericReportFile"

    report_type = factory.SubFactory(GenericReportTypeFactory)
    file = None
    year = 2020
    month = 1
    report_format = ["pdf", "txt"]


class ReportVariableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "reports.ReportVariable"

    report_type = factory.SubFactory(GenericReportTypeFactory)
    name = factory.Sequence(lambda n: f"test_variable_{n}")
    description = factory.Sequence(lambda n: f"test_variable_description_{n}")
    variable_type = "str"
    value = factory.Sequence(lambda n: f"test_variable_value_{n}")
    order = factory.Sequence(lambda n: n)

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

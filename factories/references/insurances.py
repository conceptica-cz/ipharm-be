import factory
from references.models.insurances import InsuranceCompany


class InsuranceCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InsuranceCompany
        django_get_or_create = ("code",)

    code = factory.Iterator(range(1, 8))
    name = factory.Faker("company", locale="cs")

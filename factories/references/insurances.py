import factory
from references.models.insurances import InsuranceCompany


class InsuranceCompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InsuranceCompany
        django_get_or_create = ("code",)

    code = factory.Iterator(range(1, 8))
    name = factory.LazyAttribute(lambda o: "Insurance Company {}".format(o.code))
    address = factory.Faker("street_address", locale="cs")
    zip = factory.Faker("postcode", locale="cs")
    city = factory.Faker("city", locale="cs")
    ico = factory.Faker("ean13", locale="cs")
    dic = factory.Faker("ean13", locale="cs")
    databox = factory.Faker("ean8", locale="cs")
    type = factory.Iterator(["1", "2", "3", "4"])

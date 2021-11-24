import factory
from references.models import Identification


class IdentificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Identification
        django_get_or_create = ["identifier"]

    name = factory.Sequence(lambda n: f"ZZ {n}")
    identifier = factory.Sequence(lambda n: n)
    address = factory.Faker("street_address", locale="cs")
    zip = factory.Faker("postcode", locale="cs")
    city = factory.Faker("city", locale="cs")
    ico = factory.Faker("ean13", locale="cs")
    dic = factory.Faker("ean13", locale="cs")

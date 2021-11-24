import factory
from references.models import AdverseEffect


class AdverseEffectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdverseEffect
        django_get_or_create = ["name"]

    name = factory.Faker("text", max_nb_chars=50, locale="la")

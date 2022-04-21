import itertools

import factory
from references.models.drugs import Drug


class DrugFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Drug
        django_get_or_create = ("code_sukl",)

    code_sukl = factory.Iterator(range(1, 2000))
    name = factory.Faker("sentence", nb_words=3, locale="la")
    atc_group = factory.Iterator(
        a1 + a2 for a1, a2 in itertools.product("ABCDEF", repeat=2)
    )

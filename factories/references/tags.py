import factory
from references.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ["name"]

    name = factory.Faker("word", locale="la")
    description = factory.Faker("sentence", locale="la")

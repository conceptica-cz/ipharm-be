import factory
from references.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: "Tag %d" % n)
    description = factory.Faker("sentence", locale="la")

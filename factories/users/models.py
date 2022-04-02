import factory
import users.models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = users.models.User
        django_get_or_create = ("username",)

    username = factory.sequence(lambda n: f"user_{n}")
    email = factory.sequence(lambda n: f"user_{n}@example.com")
    first_name = factory.Faker("first_name", locale="cs")
    last_name = factory.Faker("last_name", locale="cs")

import factory

import users.models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = users.models.User

    username = factory.sequence(lambda n: f"user_{n}")
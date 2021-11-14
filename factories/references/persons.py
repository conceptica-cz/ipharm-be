import factory
from references.models.persons import Person


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person
        django_get_or_create = ["person_number"]

    person_number = factory.Iterator(range(1, 100))
    name = factory.Faker("name", locale="cs")
    f_title = factory.Iterator(["Mgr.", "Ing.", "PhD."])

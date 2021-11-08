import factory
from references.models.diagnoses import Diagnosis


class DiagnosisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Diagnosis
        django_get_or_create = ("code",)

    code = factory.Iterator(range(1, 4000))
    name = factory.Faker("sentence", nb_words=2, locale="la")

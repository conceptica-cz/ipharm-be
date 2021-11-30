import factory

from factories.ipharm import CareFactory


class PatientInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "ipharm.PatientInformation"

    care = factory.SubFactory(CareFactory)
    name = factory.Faker("text", max_nb_chars=200, locale="la")
    text = factory.Faker("text", locale="la")

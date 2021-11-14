from django.test import TestCase
from references.models import Person

from factories.references.persons import PersonFactory


class PersonManagerTest(TestCase):
    # Test BaseTemporaryCreatableManager methods
    def test_get_or_create_tmp__existing(self):
        """Test that get_or_create_tmp return existing object"""

        initial_person = PersonFactory()

        person, created = Person.objects.get_or_create_temporary(
            person_number=initial_person.person_number
        )

        self.assertEqual(created, False)
        self.assertEqual(
            person,
            initial_person,
        )

    def test_get_or_create_tmp__new(self):
        """Test that get_or_create_tmp create new temporary object"""

        person, created = Person.objects.get_or_create_temporary(person_number="42")

        self.assertEqual(created, True)
        self.assertEqual(person.person_number, "42")
        self.assertEqual(person.name, "TMP")

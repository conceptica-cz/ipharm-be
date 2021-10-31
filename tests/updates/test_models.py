from django.test import TestCase
from updates.models import Reference

from factories.updates.updates import ReferenceFactory


class ReferenceManagerTest(TestCase):
    def test_get_or_create_from_settings__create(self):
        """Test that method create new instance"""
        reference = Reference.objects.get_or_create_from_settings(model_name="Clinic")

        self.assertEqual(reference.model, "Clinic")
        self.assertEqual(reference.name, "Clinics")

    def test_get_or_create_from_settings__update(self):
        """Test that method update existing instance"""
        ReferenceFactory()

        self.assertEqual(Reference.objects.count(), 1)
        reference = Reference.objects.get_or_create_from_settings(model_name="Clinic")

        self.assertEqual(Reference.objects.count(), 1)
        self.assertEqual(reference.model, "Clinic")
        self.assertEqual(reference.name, "Clinics")

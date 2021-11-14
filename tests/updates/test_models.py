from django.test import TestCase, override_settings
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

        count = Reference.objects.count()
        model_name = Reference.objects.first().model
        reference = Reference.objects.get_or_create_from_settings(model_name=model_name)

        self.assertEqual(Reference.objects.count(), count)
        self.assertEqual(reference.model, model_name)

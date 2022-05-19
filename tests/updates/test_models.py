from unittest.mock import Mock, call, patch

from django.test import TestCase, override_settings
from django.utils import timezone
from updates.models import ModelUpdate, Source, Update

from factories.updates.updates import SourceFactory, UpdateFactory


class SourceManagerTest(TestCase):
    def test_get_or_create_from_settings__create(self):
        """Test that method create new instance"""
        reference = Source.objects.get_or_create_from_settings(name="Clinic")

        self.assertEqual(reference.name, "Clinic")

    def test_get_or_create_from_settings__update(self):
        """Test that method update existing instance"""
        SourceFactory()

        count = Source.objects.count()
        name = Source.objects.first().name
        source = Source.objects.get_or_create_from_settings(name=name)

        self.assertEqual(Source.objects.count(), count)
        self.assertEqual(source.name, name)

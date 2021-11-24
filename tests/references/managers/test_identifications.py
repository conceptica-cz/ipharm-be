from django.test import TestCase, override_settings
from references.models import Identification

from factories.references import IdentificationFactory


class IdentificationManagerTest(TestCase):
    def setUp(self) -> None:
        self.some_identification = IdentificationFactory(identifier=1)
        self.our_identification = IdentificationFactory(identifier=2)

    @override_settings(OUR_HEALTH_CARE_IDENTIFIER=2)
    def test_get_our_identification(self):
        self.assertEqual(
            Identification.objects.get_our_identification(), self.our_identification
        )

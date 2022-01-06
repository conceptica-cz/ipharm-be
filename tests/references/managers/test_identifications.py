from django.test import TestCase, override_settings
from references.models import Identification

from factories.references import IdentificationFactory


class IdentificationManagerTest(TestCase):
    def setUp(self) -> None:
        identification = IdentificationFactory(identifier=1)
        self.identification_for_report = IdentificationFactory(
            identifier=2, for_insurance=True
        )
        identification = IdentificationFactory(identifier=3)

    @override_settings(OUR_HEALTH_CARE_IDENTIFIER=2)
    def test_get_our_identification(self):
        self.assertEqual(
            Identification.objects.get_identification_for_insurance_report(),
            self.identification_for_report,
        )

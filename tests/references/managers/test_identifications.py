from django.test import TestCase
from references.managers.identifications import IdentificationForReportNotFound
from references.models import Identification

from factories.references import IdentificationFactory


class IdentificationManagerTest(TestCase):
    def test_get_identification_for_insurance_report(self):
        identification = IdentificationFactory(identifier=2, for_insurance=True)
        self.assertEqual(
            Identification.objects.get_identification_for_insurance_report(),
            identification,
        )

    def test_get_identification_for_insurance_report__raise_exception__without_identification(
        self,
    ):
        """
        Test that the method raises the IdentificationForReportNotFound an exception
        if there is no identification with for_insurance=True
        """
        identification = IdentificationFactory(identifier=2, for_insurance=False)
        with self.assertRaises(IdentificationForReportNotFound):
            Identification.objects.get_identification_for_insurance_report()

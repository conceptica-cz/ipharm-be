from django.test import TestCase
from references.models import Diagnosis

from factories.references.diagnoses import DiagnosisFactory


class DiagnosisManagerTest(TestCase):
    # Test BaseTemporaryCreatableManager methods
    def test_get_or_create_tmp__existing(self):
        """Test that get_or_create_tmp return existing object"""

        initial_diagnosis = DiagnosisFactory()

        diagnosis, created = Diagnosis.objects.get_or_create_temporary(
            code=initial_diagnosis.code
        )

        self.assertEqual(created, False)
        self.assertEqual(
            diagnosis,
            initial_diagnosis,
        )

    def test_get_or_create_tmp__new(self):
        """Test that get_or_create_tmp create new temporary object"""

        diagnosis, created = Diagnosis.objects.get_or_create_temporary(code="42")

        self.assertEqual(created, True)
        self.assertEqual(diagnosis.code, "42")
        self.assertEqual(diagnosis.name, "TMP")

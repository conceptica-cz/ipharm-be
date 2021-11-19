from django.test import TestCase
from ipharm.models import Care
from ipharm.serializers.cares import CareNestedSerializer
from ipharm.serializers.patients import PatientNestedSerializer
from references.serializers.insurances import InsuranceCompanySerializer

from factories.ipharm import CareFactory
from factories.ipharm.patients import PatientFactory


class PatientNestedSerializerTest(TestCase):
    def setUp(self) -> None:
        self.patient = PatientFactory()
        self.hospital_care = CareFactory(
            patient=self.patient, care_type=Care.HOSPITALIZATION
        )
        self.ambulance_care = CareFactory(
            patient=self.patient, care_type=Care.AMBULATION
        )

    def test_insurance_company_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        insurance_company_serializer = InsuranceCompanySerializer(
            instance=self.patient.insurance_company
        )
        self.assertEqual(
            serializer.data["insurance_company"], insurance_company_serializer.data
        )

    def test_current_care_is_nested(self):
        serializer = PatientNestedSerializer(instance=self.patient)
        serializer_ambulance_care = CareNestedSerializer(instance=self.ambulance_care)
        self.assertEqual(
            serializer.data["current_ambulance_care"], serializer_ambulance_care.data
        )
        serializer_hospital_care = CareNestedSerializer(instance=self.hospital_care)
        self.assertEqual(
            serializer.data["current_hospital_care"], serializer_hospital_care.data
        )

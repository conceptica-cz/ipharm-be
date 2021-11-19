from django.test import TestCase
from ipharm.filters import PatientFilter
from ipharm.models import Care, Patient

from factories.ipharm import CareFactory, PatientFactory
from factories.references import ClinicFactory


class PatientFilterTest(TestCase):
    def setUp(self) -> None:
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.patient_0 = PatientFactory()

        self.patient_1_hospital_1 = PatientFactory()
        CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_1_hospital_1,
            clinic=self.clinic_1,
        )

        self.patient_2_hospital_1 = PatientFactory()
        CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_2_hospital_1,
            clinic=self.clinic_1,
        )

        self.patient_3_hospital_2 = PatientFactory()
        CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_3_hospital_2,
            clinic=self.clinic_2,
        )

        self.patient_4_hospital_2_ambulance_2 = PatientFactory()
        CareFactory(
            care_type=Care.HOSPITALIZATION,
            patient=self.patient_4_hospital_2_ambulance_2,
            clinic=self.clinic_2,
        )
        CareFactory(
            care_type=Care.AMBULATION,
            patient=self.patient_4_hospital_2_ambulance_2,
            clinic=self.clinic_2,
        )

        self.patient_5_ambulance_1 = PatientFactory()
        CareFactory(
            care_type=Care.AMBULATION,
            patient=self.patient_5_ambulance_1,
            clinic=self.clinic_1,
        )

        self.patient_6_ambulance_2 = PatientFactory()
        CareFactory(
            care_type=Care.AMBULATION,
            patient=self.patient_6_ambulance_2,
            clinic=self.clinic_2,
        )

    def test_hospital(self):
        """
        Test 'hospital' filter
        """
        f = PatientFilter(data={"hospital": self.clinic_1.id})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [self.patient_1_hospital_1, self.patient_2_hospital_1],
            transform=lambda x: x,
            ordered=False,
        )

        f = PatientFilter(data={"hospital": self.clinic_2.id})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [self.patient_3_hospital_2, self.patient_4_hospital_2_ambulance_2],
            transform=lambda x: x,
            ordered=False,
        )

    def test_ambulance(self):
        """
        Test 'ambulance' filter
        """
        f = PatientFilter(data={"ambulance": self.clinic_1.id})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [self.patient_5_ambulance_1],
            transform=lambda x: x,
            ordered=False,
        )

        f = PatientFilter(data={"ambulance": self.clinic_2.id})
        queryset = f.qs
        self.assertQuerysetEqual(
            queryset,
            [self.patient_6_ambulance_2, self.patient_4_hospital_2_ambulance_2],
            transform=lambda x: x,
            ordered=False,
        )

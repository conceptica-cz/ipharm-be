from django.test import TestCase

from factories.ipharm.patients import AmbulanceFactory, ClinicFactory
from factories.users import UserFactory
from users.serializers import UserSerializer


class UserSerializerTest(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.clinic_3 = ClinicFactory()
        self.ambulance_1 = AmbulanceFactory()
        self.ambulance_2 = AmbulanceFactory()

    def test_clinics_read(self):
        self.user.clinics.add(self.clinic_1)
        self.user.clinics.add(self.clinic_3)
        self.user.clinics.add(self.ambulance_2)
        self.user.save()

        user_serializer = UserSerializer(instance=self.user)

        self.assertEqual(
            user_serializer.data["clinics"],
            [self.clinic_1.pk, self.clinic_3.pk, self.ambulance_2.pk],
        )

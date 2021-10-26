from django.test import TestCase
from references.serializers.clinics import ClinicSerializer
from users.serializers import UserSerializer, UserWriteSerializer

from factories.references.clinics import AmbulanceFactory, ClinicFactory
from factories.users import UserFactory


class UserSerializerTest(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.user = UserFactory()
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.clinic_3 = ClinicFactory()
        self.ambulance_1 = AmbulanceFactory()
        self.ambulance_2 = AmbulanceFactory()
        self.user.clinics.add(self.clinic_1)
        self.user.clinics.add(self.clinic_3)
        self.user.clinics.add(self.ambulance_2)
        self.user.save()

    def test_clinics_read(self):

        user_serializer = UserSerializer(instance=self.user)

        self.assertEqual(
            user_serializer.data["clinics"],
            [
                ClinicSerializer(instance=self.clinic_1).data,
                ClinicSerializer(instance=self.clinic_3).data,
                ClinicSerializer(instance=self.ambulance_2).data,
            ],
        )

    def test_clinics_write(self):

        user_serializer = UserWriteSerializer(
            instance=self.user,
            data={"clinics": [self.clinic_1.pk, self.clinic_2.pk, self.ambulance_1.pk]},
            partial=True,
        )

        user_serializer.is_valid()
        user_serializer.save()

        self.user.refresh_from_db()
        self.assertQuerysetEqual(
            self.user.clinics.all(),
            [self.clinic_1, self.clinic_2, self.ambulance_1],
            transform=lambda c: c,
            ordered=False,
        )

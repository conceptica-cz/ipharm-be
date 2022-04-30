from django.urls import reverse
from references.serializers.clinics import ClinicSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.clinics import ClinicFactory
from factories.users import UserFactory


class UserViewTest(APITestCase):
    def setUp(self) -> None:
        self.hospital_1 = ClinicFactory(
            description="hospital_1", is_hospital=True, is_ambulance=False
        )
        self.hospital_2 = ClinicFactory(
            description="hospital_2", is_hospital=True, is_ambulance=False
        )
        self.ambulance_1 = ClinicFactory(
            description="ambulance_1", is_hospital=False, is_ambulance=True
        )
        self.ambulance_2 = ClinicFactory(
            description="ambulance_2", is_hospital=False, is_ambulance=True
        )
        self.both_1 = ClinicFactory(
            description="both_2", is_hospital=True, is_ambulance=True
        )
        self.both_2 = ClinicFactory(
            description="both_2", is_hospital=True, is_ambulance=True
        )

        self.user = UserFactory()
        self.user.hospitals.add(self.hospital_1, self.both_1)
        self.user.ambulances.add(self.ambulance_1, self.both_1, self.both_2)
        self.user.save()

    def test_get_unauthorized(self):
        response = self.client.get(reverse("users:user"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("users:user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(
            response.data["hospitals"],
            [
                ClinicSerializer(self.both_1).data,
                ClinicSerializer(self.hospital_1).data,
            ],
        )
        self.assertEqual(
            response.data["ambulances"],
            [
                ClinicSerializer(self.ambulance_1).data,
                ClinicSerializer(self.both_1).data,
                ClinicSerializer(self.both_2).data,
            ],
        )

    def test_patch(self):
        self.client.force_login(user=self.user)
        response = self.client.patch(
            reverse("users:user"),
            data={
                "hospitals": [self.hospital_2.pk, self.both_1.pk],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["hospitals"],
            [
                self.both_1.pk,
                self.hospital_2.pk,
            ],
        )
        self.assertEqual(
            response.data["ambulances"],
            [
                self.ambulance_1.pk,
                self.both_1.pk,
                self.both_2.pk,
            ],
        )

        self.user.refresh_from_db()

        self.assertQuerysetEqual(
            self.user.hospitals.all(),
            [self.hospital_2.pk, self.both_1.pk],
            transform=lambda c: c.pk,
            ordered=False,
        )

    def test_put(self):
        self.client.force_login(user=self.user)
        response = self.client.put(
            reverse("users:user"),
            data={
                "hospitals": [self.hospital_2.pk, self.both_1.pk],
                "ambulances": [self.ambulance_2.pk, self.both_1.pk],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["hospitals"],
            [
                self.both_1.pk,
                self.hospital_2.pk,
            ],
        )

        self.assertEqual(
            response.data["ambulances"],
            [
                self.ambulance_2.pk,
                self.both_1.pk,
            ],
        )

        self.user.refresh_from_db()

        self.assertQuerysetEqual(
            self.user.hospitals.all(),
            [self.hospital_2.pk, self.both_1.pk],
            transform=lambda c: c.pk,
            ordered=False,
        )
        self.assertQuerysetEqual(
            self.user.ambulances.all(),
            [self.ambulance_2.pk, self.both_1.pk],
            transform=lambda c: c.pk,
            ordered=False,
        )

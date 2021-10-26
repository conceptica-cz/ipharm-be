from django.urls import reverse
from references.serializers.clinics import ClinicSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.clinics import AmbulanceFactory, ClinicFactory
from factories.users import UserFactory


class UserViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.clinic_3 = ClinicFactory()
        self.ambulance_1 = AmbulanceFactory()
        self.ambulance_2 = AmbulanceFactory()
        self.user.clinics.add(self.clinic_1, self.clinic_3, self.ambulance_2)
        self.user.save()

    def test_get_unauthorized(self):
        response = self.client.get(reverse("user"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(
            response.data["clinics"],
            [
                ClinicSerializer(self.clinic_1).data,
                ClinicSerializer(self.clinic_3).data,
                ClinicSerializer(self.ambulance_2).data,
            ],
        )

    def test_patch_clinics(self):
        self.client.force_login(user=self.user)
        response = self.client.patch(
            reverse("user"), data={"clinics": [self.clinic_1.pk, self.clinic_2.pk]}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            {
                "username": self.user.username,
                "clinics": [self.clinic_1.pk, self.clinic_2.pk],
            },
        )

        self.user.refresh_from_db()

        self.assertQuerysetEqual(
            self.user.clinics.all(),
            [self.clinic_1.pk, self.clinic_2.pk],
            transform=lambda c: c.pk,
            ordered=False,
        )

    def test_put(self):
        self.client.force_login(user=self.user)
        response = self.client.put(
            reverse("user"), data={"clinics": [self.clinic_1.pk, self.clinic_2.pk]}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data,
            {
                "username": self.user.username,
                "clinics": [self.clinic_1.pk, self.clinic_2.pk],
            },
        )

        self.user.refresh_from_db()

        self.assertQuerysetEqual(
            self.user.clinics.all(),
            [self.clinic_1.pk, self.clinic_2.pk],
            transform=lambda c: c.pk,
            ordered=False,
        )

from unittest.mock import Mock, patch

from django.urls import reverse
from django.utils import timezone
from references.models import Person
from references.serializers.persons import PersonSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.persons import PersonFactory
from factories.users.models import UserFactory


class GetAllPersonsTest(APITestCase):
    def test_get_all_persons(self):
        PersonFactory()
        PersonFactory()
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(reverse("person_list"))
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSinglePersonTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.person_1 = PersonFactory()
        self.person_2 = PersonFactory()
        self.person_3 = PersonFactory()

    def test_get_valid_single_person(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("person_detail", kwargs={"pk": self.person_2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = PersonSerializer(self.person_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_person(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("person_detail", kwargs={"pk": 42}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

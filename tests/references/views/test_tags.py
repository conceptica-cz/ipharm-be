from unittest.mock import Mock, patch

from django.urls import reverse
from references.models import Tag
from references.serializers import TagSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.tags import TagFactory
from factories.users.models import UserFactory


class GetAllTagTest(APITestCase):
    def test_get_all_tags(self):
        TagFactory()
        TagFactory()
        user = UserFactory()
        self.client.force_login(user=user)
        response = self.client.get(reverse("references:tag_list"))
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class GetSingleTagTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.tag_1 = TagFactory()
        self.tag_2 = TagFactory()
        self.tag_3 = TagFactory()

    def test_get_valid_single_tag(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:tag_detail", kwargs={"pk": self.tag_2.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = TagSerializer(self.tag_2)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_tag(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("references:tag_detail", kwargs={"pk": self.tag_3.id + 1})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

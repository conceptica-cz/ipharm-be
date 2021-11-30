from django.urls import reverse
from ipharm.models import PharmacologicalPlan
from references.serializers import TagSerializer
from references.serializers.drugs import DrugSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import CareFactory, PharmacologicalPlanFactory
from factories.references import DrugFactory, TagFactory
from factories.users.models import UserFactory


class CreatePharmacologicalPlanTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory(checkin=None)
        PharmacologicalPlan.objects.all().delete()

    def test_create_history(self):
        self.client.force_login(user=self.user)
        drug_1 = DrugFactory()
        drug_2 = DrugFactory()
        drug_3 = DrugFactory()
        drug_4 = DrugFactory()
        tag_1 = TagFactory()
        tag_2 = TagFactory()
        tag_3 = TagFactory()
        data = {
            "care": self.care.pk,
            "text": "text",
            "tags": [tag_1.pk, tag_3.pk],
        }

        response = self.client.post(reverse("pharmacological_plan_list"), data=data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        pharmacological_plan = PharmacologicalPlan.objects.get(pk=response.data["id"])
        self.assertEqual(pharmacological_plan.care, self.care)
        self.assertEqual(pharmacological_plan.text, "text")
        self.assertEqual(pharmacological_plan.tags.count(), 2)


class GetPharmacologicalPlanTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.pharmacological_plan = PharmacologicalPlanFactory()

    def test_get_checking(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse(
                "pharmacological_plan_detail",
                kwargs={"pk": self.pharmacological_plan.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data["id"], self.pharmacological_plan.pk)
        self.assertEqual(response.data["care"], self.pharmacological_plan.care.pk)
        self.assertEqual(response.data["text"], self.pharmacological_plan.text)
        self.assertEqual(
            response.data["tags"],
            [
                TagSerializer(instance=drug).data
                for drug in self.pharmacological_plan.tags.all()
            ],
        )


class UpdatePharmacologicalPlanTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.pharmacological_plan = PharmacologicalPlanFactory(text="old text")

    def test_patch_checking(self):
        self.client.force_login(user=self.user)
        data = {
            "text": "new text",
        }

        response = self.client.patch(
            reverse(
                "pharmacological_plan_detail",
                kwargs={"pk": self.pharmacological_plan.pk},
            ),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pharmacological_plan = PharmacologicalPlan.objects.get(pk=response.data["id"])
        self.assertEqual(pharmacological_plan.text, "new text")

from django.urls import reverse
from ipharm.models.pharmacological_plans import (
    PharmacologicalPlan,
    PharmacologicalPlanComment,
)
from ipharm.serializers.pharmacological_plans import (
    PharmacologicalPlanCommentSerializer,
)
from references.serializers import TagSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import (
    CareFactory,
    PharmacologicalPlanCommentFactory,
    PharmacologicalPlanFactory,
)
from factories.references import DrugFactory, TagFactory
from factories.users.models import UserFactory


class CreatePharmacologicalPlanTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory(checkin=None)
        PharmacologicalPlan.objects.all().delete()

    def test_create_plan(self):
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

        response = self.client.post(
            reverse("ipharm:pharmacological_plan_list"), data=data
        )

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
                "ipharm:pharmacological_plan_detail",
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
        self.assertEqual(
            response.data["comments"],
            [
                PharmacologicalPlanCommentSerializer(instance=comment).data
                for comment in self.pharmacological_plan.comments.all()
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
                "ipharm:pharmacological_plan_detail",
                kwargs={"pk": self.pharmacological_plan.pk},
            ),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pharmacological_plan = PharmacologicalPlan.objects.get(pk=response.data["id"])
        self.assertEqual(pharmacological_plan.text, "new text")


class CreatePharmacologicalPlanCommentTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.pharmacological_plan = PharmacologicalPlanFactory()
        PharmacologicalPlanComment.objects.all().delete()

    def test_create_comment(self):
        self.client.force_login(user=self.user)
        data = {
            "pharmacological_plan": self.pharmacological_plan.pk,
            "text": "Test comment",
        }
        response = self.client.post(
            reverse("ipharm:pharmacological_plan_comment_list"), data=data
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )

    def test_that_only_two_verification_comments_can_be_created(self):
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=self.pharmacological_plan, comment_type="verification"
        )
        PharmacologicalPlanCommentFactory(
            pharmacological_plan=self.pharmacological_plan, comment_type="verification"
        )

        self.client.force_login(user=self.user)
        data = {
            "pharmacological_plan": self.pharmacological_plan.pk,
            "text": "Test comment",
            "comment_type": "verification",
        }
        response = self.client.post(
            reverse("ipharm:pharmacological_plan_comment_list"), data=data
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data
        )


class GetPharmacologicalPlanCommentListTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

        self.pharmacological_plan_2 = PharmacologicalPlanFactory()
        PharmacologicalPlanComment.objects.all().delete()
        self.comment_1_1 = PharmacologicalPlanCommentFactory(
            pharmacological_plan=self.pharmacological_plan_2
        )
        self.comment_1_2 = PharmacologicalPlanCommentFactory(
            pharmacological_plan=self.pharmacological_plan_2
        )

        self.pharmacological_plan_2 = PharmacologicalPlanFactory()
        PharmacologicalPlanComment.objects.all().delete()
        self.comment_2_1 = PharmacologicalPlanCommentFactory(
            pharmacological_plan=self.pharmacological_plan_2
        )
        self.comment_2_2 = PharmacologicalPlanCommentFactory(
            pharmacological_plan=self.pharmacological_plan_2
        )

    def test_get_comment_list(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("ipharm:pharmacological_plan_comment_list")
            + f"?pharmacological_plan={self.pharmacological_plan_2.pk}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            [
                PharmacologicalPlanCommentSerializer(instance=comment).data
                for comment in PharmacologicalPlanComment.objects.filter(
                    pharmacological_plan=self.pharmacological_plan_2
                )
            ],
        )


class GetPharmacologicalPlanCommentTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

        self.pharmacological_plan_comment = PharmacologicalPlanCommentFactory()

    def test_get_comment(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse(
                "ipharm:pharmacological_plan_comment_detail",
                kwargs={"pk": self.pharmacological_plan_comment.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            PharmacologicalPlanCommentSerializer(
                instance=self.pharmacological_plan_comment
            ).data,
        )


class UpdatePharmacologicalPlanCommentTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

        self.pharmacological_plan_comment = PharmacologicalPlanCommentFactory(
            text="old_text"
        )

    def test_get_comment(self):
        self.client.force_login(user=self.user)

        data = {
            "text": "new_text",
        }

        response = self.client.patch(
            reverse(
                "ipharm:pharmacological_plan_comment_detail",
                kwargs={"pk": self.pharmacological_plan_comment.pk},
            ),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.pharmacological_plan_comment.refresh_from_db()
        self.assertEqual(self.pharmacological_plan_comment.text, "new_text")

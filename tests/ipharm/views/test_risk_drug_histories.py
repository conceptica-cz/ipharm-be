from django.urls import reverse
from ipharm.models import RiskDrugHistory, RiskDrugHistoryComment
from ipharm.serializers import RiskDrugHistoryCommentSerializer
from references.serializers.drugs import DrugSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import (
    CareFactory,
    RiskDrugHistoryCommentFactory,
    RiskDrugHistoryFactory,
)
from factories.references import DrugFactory, TagFactory
from factories.users.models import UserFactory


class CreateRiskDrugHistoryTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory(checkin=None)
        RiskDrugHistory.objects.all().delete()

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
            "has_risk_drug": True,
            "risk_drugs": [drug_1.pk, drug_3.pk, drug_4.pk],
            "tags": [tag_1.pk, tag_3.pk],
        }

        response = self.client.post(reverse("risk_drug_history_list"), data=data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        risk_drug_history = RiskDrugHistory.objects.get(pk=response.data["id"])
        self.assertEqual(risk_drug_history.care, self.care)
        self.assertEqual(risk_drug_history.has_risk_drug, True)
        self.assertEqual(risk_drug_history.risk_drugs.count(), 3)
        self.assertEqual(risk_drug_history.tags.count(), 2)


class GetRiskDrugHistoryTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.risk_drug_history = RiskDrugHistoryFactory()

    def test_get_checking(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse(
                "risk_drug_history_detail", kwargs={"pk": self.risk_drug_history.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data["id"], self.risk_drug_history.pk)
        self.assertEqual(response.data["care"], self.risk_drug_history.care.pk)
        self.assertEqual(
            response.data["has_risk_drug"], self.risk_drug_history.has_risk_drug
        )
        self.assertEqual(
            response.data["risk_drugs"],
            [
                DrugSerializer(instance=drug).data
                for drug in self.risk_drug_history.risk_drugs.all()
            ],
        ),
        self.assertEqual(
            response.data["comments"],
            [
                RiskDrugHistoryCommentSerializer(instance=comment).data
                for comment in self.risk_drug_history.comments.all()
            ],
        )


class UpdateRiskDrugHistoryTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.risk_drug_history = RiskDrugHistoryFactory(has_risk_drug=False)

    def test_patch_checking(self):
        self.client.force_login(user=self.user)
        data = {
            "has_risk_drug": True,
        }

        response = self.client.patch(
            reverse(
                "risk_drug_history_detail", kwargs={"pk": self.risk_drug_history.pk}
            ),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        risk_drug_history = RiskDrugHistory.objects.get(pk=response.data["id"])
        self.assertEqual(risk_drug_history.has_risk_drug, True)


class CreateRiskDrugHistoryCommentTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.risk_drug_history = RiskDrugHistoryFactory()
        RiskDrugHistoryComment.objects.all().delete()

    def test_create_comment(self):
        self.client.force_login(user=self.user)
        data = {
            "risk_drug_history": self.risk_drug_history.pk,
            "text": "Test comment",
        }
        response = self.client.post(
            reverse("risk_drug_history_comment_list"), data=data
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )


class GetRiskDrugHistoryCommentListTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

        self.risk_drug_history_2 = RiskDrugHistoryFactory()
        RiskDrugHistoryComment.objects.all().delete()
        self.comment_1_1 = RiskDrugHistoryCommentFactory(
            risk_drug_history=self.risk_drug_history_2
        )
        self.comment_1_2 = RiskDrugHistoryCommentFactory(
            risk_drug_history=self.risk_drug_history_2
        )

        self.risk_drug_history_2 = RiskDrugHistoryFactory()
        RiskDrugHistoryComment.objects.all().delete()
        self.comment_2_1 = RiskDrugHistoryCommentFactory(
            risk_drug_history=self.risk_drug_history_2
        )
        self.comment_2_2 = RiskDrugHistoryCommentFactory(
            risk_drug_history=self.risk_drug_history_2
        )

    def test_get_comment_list(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("risk_drug_history_comment_list")
            + f"?risk_drug_history={self.risk_drug_history_2.pk}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"],
            [
                RiskDrugHistoryCommentSerializer(instance=comment).data
                for comment in RiskDrugHistoryComment.objects.filter(
                    risk_drug_history=self.risk_drug_history_2
                )
            ],
        )


class GetRiskDrugHistoryCommenTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

        self.risk_drug_history_comment = RiskDrugHistoryCommentFactory()

    def test_get_comment(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse(
                "risk_drug_history_comment_detail",
                kwargs={"pk": self.risk_drug_history_comment.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            RiskDrugHistoryCommentSerializer(
                instance=self.risk_drug_history_comment
            ).data,
        )


class UpdateRiskDrugHistoryCommenTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

        self.risk_drug_history_comment = RiskDrugHistoryCommentFactory(text="old_text")

    def test_get_comment(self):
        self.client.force_login(user=self.user)

        data = {
            "text": "new_text",
        }

        response = self.client.patch(
            reverse(
                "risk_drug_history_comment_detail",
                kwargs={"pk": self.risk_drug_history_comment.pk},
            ),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.risk_drug_history_comment.refresh_from_db()
        self.assertEqual(self.risk_drug_history_comment.text, "new_text")

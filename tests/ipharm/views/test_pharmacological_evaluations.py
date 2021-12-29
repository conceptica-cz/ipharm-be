from django.urls import reverse
from ipharm.models import PharmacologicalEvaluation
from references.serializers import TagSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from updates.serializers import ModelChangeSerializer

from factories.ipharm import CareFactory, PharmacologicalEvaluationFactory
from factories.references import DrugFactory, TagFactory
from factories.users.models import UserFactory


class CreatePharmacologicalEvaluationTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.care = CareFactory(checkin=None)
        PharmacologicalEvaluation.objects.all().delete()

    def test_create_history(self):
        self.client.force_login(user=self.user)
        drug = DrugFactory()
        tag_1 = TagFactory()
        tag_2 = TagFactory()
        tag_3 = TagFactory()
        data = {
            "care": self.care.pk,
            "drug": drug.pk,
            "deployment_initial_diagnosis": True,
            "tags": [tag_1.pk, tag_3.pk],
        }

        response = self.client.post(
            reverse("pharmacological_evaluation_list"), data=data
        )

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )
        pharmacological_evaluation = PharmacologicalEvaluation.objects.get(
            pk=response.data["id"]
        )
        self.assertEqual(pharmacological_evaluation.care, self.care)
        self.assertEqual(pharmacological_evaluation.drug, drug)
        self.assertEqual(pharmacological_evaluation.deployment_initial_diagnosis, True)
        self.assertEqual(pharmacological_evaluation.tags.count(), 2)


class GetPharmacologicalEvaluationListTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.pharmacological_infomration_information = (
            PharmacologicalEvaluationFactory()
        )
        self.care_1 = CareFactory()
        self.care_2 = CareFactory()
        PharmacologicalEvaluation.objects.all().delete()

        self.pharmacological_infomration_information_1_1 = (
            PharmacologicalEvaluationFactory(care=self.care_1)
        )
        self.pharmacological_infomration_information_1_2 = (
            PharmacologicalEvaluationFactory(care=self.care_1)
        )
        self.pharmacological_infomration_information_2_1 = (
            PharmacologicalEvaluationFactory(care=self.care_2)
        )
        self.pharmacological_infomration_information_2_2 = (
            PharmacologicalEvaluationFactory(care=self.care_2)
        )

    def test_get__care_filter(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse("pharmacological_evaluation_list"), {"care": self.care_1.pk}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(len(response.data["results"]), 2)


class GetPharmacologicalEvaluationTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.pharmacological_evaluation = PharmacologicalEvaluationFactory()

    def test_get_checking(self):
        self.client.force_login(user=self.user)

        response = self.client.get(
            reverse(
                "pharmacological_evaluation_detail",
                kwargs={"pk": self.pharmacological_evaluation.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data["id"], self.pharmacological_evaluation.pk)
        self.assertEqual(response.data["care"], self.pharmacological_evaluation.care.pk)
        self.assertEqual(response.data["drug"], self.pharmacological_evaluation.drug.pk)
        self.assertEqual(
            response.data["tags"],
            [
                TagSerializer(instance=drug).data
                for drug in self.pharmacological_evaluation.tags.all()
            ],
        )


class UpdatePharmacologicalEvaluationTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.pharmacological_evaluation = PharmacologicalEvaluationFactory(
            deployment_initial_diagnosis=False
        )

    def test_patch_checking(self):
        self.client.force_login(user=self.user)
        data = {
            "deployment_initial_diagnosis": True,
        }

        response = self.client.patch(
            reverse(
                "pharmacological_evaluation_detail",
                kwargs={"pk": self.pharmacological_evaluation.pk},
            ),
            data=data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pharmacological_evaluation = PharmacologicalEvaluation.objects.get(
            pk=response.data["id"]
        )
        self.assertEqual(pharmacological_evaluation.deployment_initial_diagnosis, True)


class GetPharmacologicalEvaluationHistoryTest(APITestCase):
    def setUp(self) -> None:
        self.user_1 = UserFactory(username="user_1")
        self.user_2 = UserFactory(username="user_2")
        self.user_3 = UserFactory(username="user_3")

        self.pharmacological_evaluation = PharmacologicalEvaluationFactory(
            deployment_initial_diagnosis=False,
            discontinuation_contradiction=True,
        )

        self.pharmacological_evaluation.deployment_initial_diagnosis = True
        self.pharmacological_evaluation.discontinuation_contradiction = False
        self.pharmacological_evaluation.save()

        history_record = self.pharmacological_evaluation.history.first()
        history_record.history_user = self.user_1
        history_record.save()

        self.pharmacological_evaluation.deployment_initial_diagnosis = False
        self.pharmacological_evaluation.save()

        history_record = self.pharmacological_evaluation.history.first()
        history_record.history_user = self.user_2
        history_record.save()

    def test_history(self):
        self.client.force_login(user=self.user_3)
        response = self.client.get(
            reverse(
                "pharmacological_evaluation_history",
                kwargs={"pk": self.pharmacological_evaluation.pk},
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data,
            [
                ModelChangeSerializer(change).data
                for change in self.pharmacological_evaluation.get_changes()
            ],
        )

from unittest.mock import patch

from django.urls import reverse
from requisitions.models.requisitions import Requisition
from requisitions.serializers.requisitions import RequisitionNestedSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.ipharm import PatientFactory
from factories.references import PersonFactory
from factories.requisitions.requisitions import RequisitionFactory
from factories.users import UserFactory


class RequisitionListTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.patient_1 = PatientFactory()
        self.patient_2 = PatientFactory()

        self.requisition_1 = RequisitionFactory(patient=self.patient_1)
        self.requisition_2 = RequisitionFactory(patient=self.patient_1)
        self.requisition_3 = RequisitionFactory(patient=self.patient_2)

    def test_get_all_requisitions(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("requisitions:requisition_list"))
        requisitions = Requisition.objects.all()
        serializer = RequisitionNestedSerializer(requisitions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_filtered_by_patient(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("requisitions:requisition_list"),
            data={"patient": self.patient_1.pk},
        )
        requisitions = Requisition.objects.filter(patient=self.patient_1)
        serializer = RequisitionNestedSerializer(requisitions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class RequisitionDetailTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.requisition = RequisitionFactory()

    def test_get_single_requisition(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(
                "requisitions:requisition_detail", kwargs={"pk": self.requisition.pk}
            )
        )
        serializer = RequisitionNestedSerializer(self.requisition)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_requisition_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("requisitions:requisition_detail", kwargs={"pk": 42})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("requisitions.views.requisitions.task_update_remote_requisition.apply_async")
    def test_patch_single_requisition(self, task_apply_async):
        self.client.force_login(user=self.user)
        new_state = Requisition.STATE_SOLVED
        solver = PersonFactory()
        response = self.client.patch(
            reverse(
                "requisitions:requisition_detail", kwargs={"pk": self.requisition.pk}
            ),
            data={
                "state": new_state,
                "solver": solver.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.requisition.refresh_from_db()
        self.assertEqual(self.requisition.state, new_state)
        self.assertEqual(self.requisition.solver, solver)

        task_apply_async.assert_called_with(
            kwargs={
                "requisition_id": self.requisition.pk,
                "fields_to_update": ["state", "solver"],
            },
            queue="high_priority",
        )

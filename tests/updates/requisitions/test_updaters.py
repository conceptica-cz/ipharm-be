from unittest.mock import patch

from django.test import TestCase, override_settings
from ipharm.models.patients import Patient
from references.models import Person
from requisitions.models import Requisition
from updates.requisitions.updaters import (
    update_local_requisition,
    update_remote_requisition,
    update_requisition,
)

from factories.ipharm import PatientFactory
from factories.references import PersonFactory
from factories.requisitions import RequisitionFactory


class UpdateLocalRequisitionTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            "id": 42,
            "patient": {
                "id": 1,
                "birth_number": "2910247869",
                "external_id": "16",
                "name": "Bartoš Arnošt",
                "first_name": "Arnošt",
                "last_name": "Bartoš",
            },
            "applicant": {
                "id": 7,
                "person_number": "7",
                "name": "Adam Kadlec",
                "f_title": "Mgr.",
                "l_title": "",
            },
            "solver": None,
            "type": "ipharm",
            "subtype": "ipharm_conciliation",
            "state": "created",
            "text": "zadanka 1",
            "file": None,
            "created_at": "2022-05-23T14:19:31.327449+02:00",
            "updated_at": None,
            "is_synced": False,
            "synced_at": None,
        }

    def test__existing_patient_and_applicant(self):
        patient = PatientFactory(birth_number="2910247869")
        person = PersonFactory(person_number="7")

        requisition, _ = update_local_requisition(self.data)

        self.assertEqual(Requisition.objects.count(), 1)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 1)

        self.assertEqual(requisition, Requisition.objects.first())

        self.assertEqual(requisition.patient, patient)
        self.assertEqual(requisition.applicant, person)
        self.assertEqual(requisition.external_id, 42)
        self.assertEqual(requisition.text, "zadanka 1")

    def test__existing_patient_and_non_existing_applicant(self):
        patient = PatientFactory(birth_number="2910247869")

        requisition, _ = update_local_requisition(self.data)

        self.assertEqual(Requisition.objects.count(), 1)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 1)

        self.assertEqual(requisition, Requisition.objects.first())

        self.assertEqual(requisition.patient, patient)
        self.assertEqual(requisition.applicant.person_number, "7")
        self.assertEqual(requisition.applicant.name, "Adam Kadlec")
        self.assertEqual(requisition.external_id, 42)
        self.assertEqual(requisition.text, "zadanka 1")

    def test__existing_requisitions(self):
        patient = PatientFactory(birth_number="2910247869")
        person = PersonFactory(person_number="7")
        existing_requisition = RequisitionFactory(
            external_id=42, patient=patient, applicant=person, solver=None
        )

        requisition, _ = update_local_requisition(self.data)

        self.assertEqual(Requisition.objects.count(), 1)
        self.assertEqual(requisition.id, existing_requisition.id)
        self.assertEqual(requisition.external_id, existing_requisition.external_id)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 1)

        self.assertEqual(requisition, Requisition.objects.first())

        self.assertEqual(requisition.patient, patient)
        self.assertEqual(requisition.applicant, person)
        self.assertEqual(requisition.external_id, 42)
        self.assertEqual(requisition.text, "zadanka 1")


class UpdateRemoveRequisitionTest(TestCase):
    @patch("updates.requisitions.updaters.requests.patch")
    def test_successful_update_set_is_synced(self, mock_patch):
        mock_patch.return_value.status_code = 200
        requisition = RequisitionFactory(is_synced=False)

        update_remote_requisition(
            requisition=requisition, fields_to_update=["state", "is_synced"]
        )

        self.assertEqual(Requisition.objects.get(id=requisition.id).is_synced, True)

    @patch("updates.requisitions.updaters.requests.patch")
    def test_unsuccessful_update_unset_is_synced(self, mock_patch):
        mock_patch.return_value.status_code = 404
        requisition = RequisitionFactory(is_synced=True)

        update_remote_requisition(
            requisition=requisition, fields_to_update=["state", "is_synced"]
        )

        self.assertEqual(Requisition.objects.get(id=requisition.id).is_synced, False)

    @patch("updates.requisitions.updaters.requests.patch")
    def test_on_exeption_update_unset_is_synced(self, mock_patch):
        mock_patch.side_effect = Exception
        requisition = RequisitionFactory(is_synced=True)

        update_remote_requisition(
            requisition=requisition, fields_to_update=["state", "is_synced"]
        )

        self.assertEqual(Requisition.objects.get(id=requisition.id).is_synced, False)


class UpdateRequisitionTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            "id": 42,
            "patient": {
                "id": 1,
                "birth_number": "2910247869",
                "external_id": "16",
                "name": "Bartoš Arnošt",
                "first_name": "Arnošt",
                "last_name": "Bartoš",
            },
            "applicant": {
                "id": 7,
                "person_number": "7",
                "name": "Adam Kadlec",
                "f_title": "Mgr.",
                "l_title": "",
            },
            "solver": None,
            "type": "ipharm",
            "subtype": "ipharm_conciliation",
            "state": "created",
            "text": "zadanka 1",
            "file": None,
            "created_at": "2022-05-23T14:19:31.327449+02:00",
            "updated_at": None,
            "is_synced": False,
            "synced_at": None,
        }

    @patch("updates.requisitions.updaters.requests.patch")
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test__existing_patient_and_applicant(self, mock_patch):
        mock_patch.return_value.status_code = 200
        patient = PatientFactory(birth_number="2910247869")
        person = PersonFactory(person_number="7")

        update_requisition(data=self.data)

        self.assertEqual(Requisition.objects.count(), 1)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 1)

        requisition = Requisition.objects.first()

        self.assertEqual(requisition.patient, patient)
        self.assertEqual(requisition.applicant, person)
        self.assertEqual(requisition.external_id, 42)
        self.assertEqual(requisition.text, "zadanka 1")
        self.assertEqual(requisition.state, Requisition.STATE_PENDING)
        self.assertEqual(requisition.is_synced, True)

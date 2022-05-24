from unittest.mock import Mock, call, patch

from django.test import TestCase, override_settings
from ipharm.models.cares import Care, Dekurz
from ipharm.models.patients import Patient
from references.models import Clinic, Department
from requisitions.models import Requisition
from updates.tasks import update

from factories.ipharm import CareFactory, PatientFactory
from factories.references import ClinicFactory, DepartmentFactory, PersonFactory


@patch("updates.bulovka.loaders.requests.get")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestPatientUpdate(TestCase):
    def test_new_patient(self, mocked_get):
        response_data = {
            "result": [
                {
                    "patientId": 42,
                    "name": "Doe John",
                    "birthNumber": "1234567890",
                    "birthDate": "1987-04-02",
                    "insuranceCompany": "111",
                    "insuranceNumber": "123456789",
                    "height": 173.0,
                    "weight": 61.0,
                    "diagnosis": "U071",
                    "hospitalizationId": 143,
                    "departmentIn": 600,
                    "dateIn": "2021-12-26 14:27",
                    "dekurzTime": "2022-01-06 09:30",
                    "dekurzWho": 70331,
                    "dekurzDepartment": 600,
                },
                {
                    "patientId": 43,
                    "name": "Smith John",
                    "birthNumber": "1234567891",
                    "birthDate": "1987-04-02",
                    "insuranceCompany": "111",
                    "insuranceNumber": "123456789",
                    "hospitalizationId": 144,
                    "height": 173.0,
                    "weight": 61.0,
                    "diagnosis": "U071",
                    "departmentIn": 600,
                    "dateIn": "2021-12-26 14:27",
                    "dekurzWho": 0,
                    "dekurzDepartment": 0,
                },
                {
                    "patientId": 44,
                    "name": "Doe John",
                    "birthNumber": "1234567892",
                    "birthDate": "1987-04-02",
                    "insuranceCompany": "111",
                    "insuranceNumber": "123456790",
                    "height": 173.0,
                    "weight": 61.0,
                    "diagnosis": "U071",
                    "hospitalizationId": 145,
                    "departmentIn": 600,
                    "dateIn": "2021-12-26 14:27",
                    "dekurzTime": "2022-01-06 09:30",
                    "dekurzWho": 0,
                    "dekurzDepartment": 601,
                },
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Patient", url_parameters={"clinicId": 1})

        self.assertEqual(Patient.objects.count(), 3)
        self.assertEqual(Care.objects.count(), 3)
        self.assertEqual(Dekurz.objects.count(), 2)

        self.assertEqual(Dekurz.objects.filter(doctor__isnull=True).count(), 1)

        patient_1 = Patient.objects.get(external_id="42")
        self.assertEqual(patient_1.name, "Doe John")
        self.assertEqual(patient_1.first_name, "John")
        self.assertEqual(patient_1.last_name, "Doe")
        self.assertEqual(patient_1.birth_number, "1234567890")
        self.assertEqual(patient_1.insurance_company.code, "111")
        self.assertEqual(patient_1.insurance_number, "123456789")
        self.assertEqual(patient_1.height, 173.0)
        self.assertEqual(patient_1.weight, 61.0)


@patch("updates.bulovka.loaders.requests.get")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestPatientCareUpdate(TestCase):
    def test_that_patient_without_unis_entity_finish_care(self, mocked_get):
        CareFactory(
            external_id=141,
            patient__birth_number="1234567880",
            is_active=True,
            finished_at=None,
            clinic__external_id=1,
            clinic__reference_id=1,
        )
        CareFactory(
            external_id=142,
            patient__birth_number="1234567890",
            is_active=True,
            finished_at=None,
            clinic__external_id=1,
            clinic__reference_id=1,
        )

        response_data = {
            "result": [
                {
                    "patientId": 42,
                    "name": "Doe John",
                    "birthNumber": "1234567890",
                    "birthDate": "1987-04-02",
                    "insuranceCompany": "111",
                    "insuranceNumber": "123456789",
                    "height": 173.0,
                    "weight": 61.0,
                    "diagnosis": "U071",
                    "hospitalizationId": 142,
                    "departmentIn": 600,
                    "dateIn": "2021-12-26 14:27",
                    "dekurzTime": "2022-01-06 09:30",
                    "dekurzWho": 70331,
                    "dekurzDepartment": 600,
                },
                {
                    "patientId": 43,
                    "name": "Smith John",
                    "birthNumber": "1234567891",
                    "birthDate": "1987-04-02",
                    "insuranceCompany": "111",
                    "insuranceNumber": "123456789",
                    "hospitalizationId": 143,
                    "height": 173.0,
                    "weight": 61.0,
                    "diagnosis": "U071",
                    "departmentIn": 600,
                    "dateIn": "2021-12-26 14:27",
                    "dekurzWho": 0,
                    "dekurzDepartment": 0,
                },
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Patient", url_parameters={"clinicId": 1})

        finished_care = Care.objects.get(external_id="141")
        updated_care = Care.objects.get(external_id="142")
        new_care = Care.objects.get(external_id="143")

        self.assertEqual(finished_care.is_active, False)
        self.assertNotEqual(finished_care.finished_at, None)
        self.assertEqual(updated_care.is_active, True)
        self.assertEqual(updated_care.finished_at, None)
        self.assertEqual(new_care.is_active, True)
        self.assertEqual(new_care.finished_at, None)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_that_new_care_created_on_external_id_change(self, mocked_get):
        """
        Test that new care is created when external id changes
        and old care is finished
        """
        CareFactory(
            external_id=141,
            patient__birth_number="1234567890",
            is_active=True,
            finished_at=None,
            clinic__external_id=1,
            clinic__reference_id=1,
        )

        response_data = {
            "result": [
                {
                    "patientId": 42,
                    "name": "Doe John",
                    "birthNumber": "1234567890",
                    "birthDate": "1987-04-02",
                    "insuranceCompany": "111",
                    "insuranceNumber": "123456789",
                    "height": 173.0,
                    "weight": 61.0,
                    "diagnosis": "U071",
                    "hospitalizationId": 142,
                    "departmentIn": 600,
                    "dateIn": "2021-12-26 14:27",
                    "dekurzTime": "2022-01-06 09:30",
                    "dekurzWho": 70331,
                    "dekurzDepartment": 600,
                },
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Patient", url_parameters={"clinicId": 1})

        finished_care = Care.objects.get(external_id="141")
        new_care = Care.objects.get(external_id="142")

        self.assertEqual(finished_care.patient, new_care.patient)
        self.assertEqual(finished_care.is_active, False)
        self.assertNotEqual(finished_care.finished_at, None)
        self.assertEqual(new_care.is_active, True)
        self.assertEqual(new_care.finished_at, None)


@patch("updates.common.loaders.requests.get")
class TestClinicUpdate(TestCase):
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_clinic(self, mocked_get):
        ClinicFactory(reference_id=20, external_id=10)
        ClinicFactory(reference_id=21, external_id=11)
        response_data = {
            "results": [
                {
                    "id": 21,
                    "external_id": 41,
                    "abbreviation": "C1",
                    "description": "Clinic 1",
                    "is_hospital": False,
                    "is_ambulance": True,
                },
                {
                    "id": 22,
                    "external_id": 42,
                    "abbreviation": "C2",
                    "description": "Clinic 2",
                    "is_hospital": True,
                    "is_ambulance": False,
                },
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Clinic")

        self.assertEqual(Clinic.objects.count(), 3)

        clinic_1 = Clinic.objects.get(reference_id=21)
        self.assertEqual(clinic_1.external_id, 41)
        self.assertEqual(clinic_1.abbreviation, "C1")
        self.assertEqual(clinic_1.description, "Clinic 1")
        self.assertEqual(clinic_1.is_hospital, False)
        self.assertEqual(clinic_1.is_ambulance, True)

        clinic_2 = Clinic.objects.get(reference_id=22)
        self.assertEqual(clinic_2.external_id, 42)
        self.assertEqual(clinic_2.abbreviation, "C2")
        self.assertEqual(clinic_2.description, "Clinic 2")
        self.assertEqual(clinic_2.is_hospital, True)
        self.assertEqual(clinic_2.is_ambulance, False)


@patch("updates.common.loaders.requests.get")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestDepartmentUpdate(TestCase):
    def test_department(self, mocked_get):
        clinic = ClinicFactory(reference_id=41, external_id=51)
        DepartmentFactory(external_id=20, clinic=clinic)
        DepartmentFactory(external_id=21, clinic=clinic)
        clinic = ClinicFactory(reference_id=42, external_id=52)
        DepartmentFactory(external_id=22, clinic=clinic)
        response_data = {
            "results": [
                {
                    "id": 1,
                    "clinic": 41,
                    "external_id": 21,
                    "abbreviation": "D1",
                    "description": "Department 1",
                    "specialization_code": "111",
                    "icp": "111111",
                },
                {
                    "id": 2,
                    "clinic": 43,
                    "external_id": 22,
                    "abbreviation": "D2",
                    "description": "Department 2",
                    "specialization_code": "222",
                    "icp": "222222",
                },
                {
                    "id": 3,
                    "clinic": 43,
                    "external_id": 23,
                    "abbreviation": "D3",
                    "description": "Department 3",
                    "specialization_code": "333",
                    "icp": "333333",
                },
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Department")

        self.assertEqual(Department.objects.count(), 4)
        self.assertEqual(Clinic.objects.count(), 3)

        clinic_1 = Clinic.objects.get(reference_id=41)
        clinic_2 = Clinic.objects.get(reference_id=42)
        clinic_3 = Clinic.objects.get(reference_id=43)

        department_1 = Department.objects.get(external_id=21)
        self.assertEqual(department_1.external_id, 21)
        self.assertEqual(department_1.abbreviation, "D1")
        self.assertEqual(department_1.description, "Department 1")
        self.assertEqual(department_1.specialization_code, "111")
        self.assertEqual(department_1.icp, "111111")
        self.assertEqual(department_1.clinic, clinic_1)

        department_2 = Department.objects.get(external_id=22)
        self.assertEqual(department_2.external_id, 22)
        self.assertEqual(department_2.abbreviation, "D2")
        self.assertEqual(department_2.description, "Department 2")
        self.assertEqual(department_2.specialization_code, "222")
        self.assertEqual(department_2.icp, "222222")
        self.assertEqual(department_2.clinic, clinic_3)

        department_3 = Department.objects.get(external_id=23)
        self.assertEqual(department_3.external_id, 23)
        self.assertEqual(department_3.abbreviation, "D3")
        self.assertEqual(department_3.description, "Department 3")
        self.assertEqual(department_3.specialization_code, "333")
        self.assertEqual(department_3.icp, "333333")
        self.assertEqual(department_3.clinic, clinic_3)


@patch("updates.common.loaders.requests.get")
@patch("updates.common.loaders.requests.patch")
class TestRequisitionUpdate(TestCase):
    maxDiff = True
    UPDATE_SOURCES = {
        "Requisition": {
            "data_loader_kwargs": {
                "url": "http://izadanky/api/v1"
                + "/requisitions/?is_synced=false&type=ipharm",
                "token": "test_token",
            },
            "model_updater": "updates.requisitions.updaters.update_requisition",
            "transformers": [],
            "queue": "medium_priority",
        },
    }

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    @override_settings(UPDATE_SOURCES=UPDATE_SOURCES)
    @override_settings(
        UPDATE_REQUISITION_URL="http://izadanky/api/v1/requisitions/{id}/"
    )
    @override_settings(IZADANKY_TOKEN="test_token")
    def test_update(self, mocked_patch, mocked_get):
        response_data = {
            "results": [
                {
                    "id": 1,
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
                },
                {
                    "id": 3,
                    "patient": {
                        "id": 3,
                        "birth_number": "0102066236",
                        "external_id": "20",
                        "name": "Bláha Jozef",
                        "first_name": "Jozef",
                        "last_name": "Bláha",
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
                    "subtype": "ipahrm_adverse_effect",
                    "state": "created",
                    "text": "zadankya 3",
                    "file": None,
                    "created_at": "2022-05-23T14:41:31.191086+02:00",
                    "updated_at": None,
                    "is_synced": False,
                    "synced_at": None,
                },
            ],
        }
        patient_1 = PatientFactory(birth_number="2910247869")
        patient_2 = PatientFactory(birth_number="0102066236")
        patient_3 = PatientFactory()
        person_1 = PersonFactory(person_number="7")
        person_2 = PersonFactory()

        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        mocked_patch.return_value = Mock(status_code=200)

        update("Requisition")

        self.assertEqual(Requisition.objects.count(), 2)

        requisition_1 = Requisition.objects.get(external_id=1)
        requisition_2 = Requisition.objects.get(external_id=3)
        self.assertEqual(requisition_1.patient, patient_1)
        self.assertEqual(requisition_1.applicant, person_1)
        self.assertEqual(requisition_1.text, "zadanka 1")
        self.assertEqual(requisition_2.patient, patient_2)
        self.assertEqual(requisition_2.applicant, person_1)
        self.assertEqual(requisition_2.text, "zadankya 3")

        self.assertEqual(
            mocked_get.mock_calls[0],
            call(
                "http://izadanky/api/v1/requisitions/?is_synced=false&type=ipharm",
                headers={"Authorization": "Bearer test_token"},
            ),
        )

        self.assertEqual(
            mocked_patch.mock_calls,
            [
                call(
                    "http://izadanky/api/v1/requisitions/1/",
                    data={"is_synced": True, "state": "pending"},
                    headers={"Authorization": "Bearer test_token"},
                ),
                call(
                    "http://izadanky/api/v1/requisitions/3/",
                    data={"is_synced": True, "state": "pending"},
                    headers={"Authorization": "Bearer test_token"},
                ),
            ],
        )
        self.assertEqual(requisition_1.is_synced, True)
        self.assertEqual(requisition_2.is_synced, True)

from unittest.mock import Mock, patch

from django.test import TestCase
from ipharm.models import Patient
from updates.models import Source
from updates.tasks import update


@patch("updates.bulovka.loaders.requests.get")
class TestPatientUpdate(TestCase):
    def test_new_patient(self, mocked_get):
        response_data = {
            "result": [
                {
                    "recordId": 828116,
                    "patientId": 1364419,
                    "firstName": "Ivana",
                    "lastName": "Testovací",
                    "birthNumber": "1234567890",
                    "birthDate": "1987-04-02",
                    "insuranceCompany": "111",
                    "insuranceNumber": "1234567890",
                    "height": 160.0,
                    "weight": 57.0,
                    "departmentIn": 16,
                    "dateIn": "2021-05-18 20:23",
                    "dateOut": None,
                    "diagnosis": "K519",
                    "dekurzTime": "2021-09-23T20:29:00",
                    "dekurzWho": 92328,
                    "dekurzDepartment": 20,
                },
                {
                    "recordId": 1413734,
                    "patientId": 1231676,
                    "firstName": "Karel",
                    "lastName": "Testovací",
                    "birthNumber": "1234567891",
                    "birthDate": "1959-05-25",
                    "insuranceCompany": "111",
                    "insuranceNumber": "1234567890 ",
                    "height": 178.0,
                    "weight": 136.0,
                    "departmentIn": 33,
                    "dateIn": "2021-07-04 15:59",
                    "dateOut": None,
                    "diagnosis": "I500",
                    "dekurzTime": "2021-09-25T10:39:00",
                    "dekurzWho": 92328,
                    "dekurzDepartment": 18,
                },
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Patient", clinic_id=1)

        self.assertEqual(Patient.objects.count(), 2)

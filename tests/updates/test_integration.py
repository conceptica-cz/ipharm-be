from unittest.mock import Mock, patch

from django.test import TestCase
from ipharm.models import Care, Dekurz, Patient
from updates.models import Source
from updates.tasks import update


@patch("updates.bulovka.loaders.requests.get")
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
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Patient", clinic_id=1)

        self.assertEqual(Patient.objects.count(), 2)
        self.assertEqual(Care.objects.count(), 2)
        self.assertEqual(Dekurz.objects.count(), 1)

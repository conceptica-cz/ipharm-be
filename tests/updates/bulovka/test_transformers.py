from unittest import TestCase

from updates.bulovka.transformers import patient_transformer


class PatientTransformerTest(TestCase):
    def test_patient_transformer(self):
        input_data = {
            "recordId": 828116,
            "patientId": 1364419,
            "name": "Testovaci Ivana",
            "birthNumber": "1234567890",
            "birthDate": "1987-04-02",
            "insuranceCompany": "111",
            "insuranceNumber": "1234567890",
            "height": 160.0,
            "weight": 57.0,
            "departmentIn": 16,
            "dateIn": "2021-05-18T20:23+00:00",
            "dateOut": None,
            "diagnosis": "K519",
            "dekurzTime": "2021-09-23T20:29:00+00:00",
            "dekurzWho": 92328,
            "dekurzDepartment": 20,
        }

        expected = {
            "patient": {
                "external_id": 1364419,
                "first_name": "Ivana",
                "last_name": "Testovaci",
                "birth_number": "1234567890",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "1234567890",
                "height": 160.0,
                "weight": 57.0,
            },
            "care": {
                "external_id": 828116,
                "department": 16,
                "started_at": "2021-05-18T20:23+00:00",
                "finished_at": None,
                "main_diagnosis": "K519",
            },
            "dekurz": {
                "made_at": "2021-09-23T20:29:00+00:00",
                "doctor": 92328,
                "department": 20,
            },
        }

        output_data = patient_transformer(input_data)

        self.assertEqual(output_data, expected)

from unittest import TestCase

from updates.bulovka.transformers import patient_transformer


class PatientTransformerTest(TestCase):
    maxDiff = None

    def test_patient_transformer(self):
        input_data = {
            "patientId": 42,
            "name": "Doe John",
            "birthNumber": "1234567890",
            "birthDate": "1987-04-02",
            "insuranceCompany": "111",
            "insuranceNumber": "123456789",
            "height": 173.0,
            "weight": 61.0,
            "diagnosis": "U071",
            "hospitalizationId": 43,
            "departmentIn": 600,
            "dateIn": "2021-12-26 14:27",
            "dekurzTime": "2022-01-06 09:30",
            "dekurzWho": 70331,
            "dekurzDepartment": 600,
        }

        expected = {
            "patient": {
                "external_id": 42,
                "first_name": "John",
                "last_name": "Doe",
                "birth_number": "1234567890",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "123456789",
                "height": 173.0,
                "weight": 61.0,
            },
            "care": {
                "external_id": 43,
                "department": 600,
                "started_at": "2021-12-26 14:27",
                "finished_at": None,
                "main_diagnosis": "U071",
            },
            "dekurz": {
                "made_at": "2022-01-06 09:30",
                "doctor": 70331,
                "department": 600,
            },
        }

        output_data = patient_transformer(input_data)

        self.assertEqual(output_data, expected)

    def test_patient_transformer__without_dekurz_and_hospitalization(self):
        input_data = {
            "patientId": 42,
            "name": "Smith John",
            "birthNumber": "1234567891",
            "birthDate": "1987-04-02",
            "insuranceCompany": "111",
            "insuranceNumber": "123456789",
            "hospitalizationId": 43,
            "height": 173.0,
            "weight": 61.0,
            "diagnosis": "U071",
            "departmentIn": 600,
            "dateIn": "2021-12-26 14:27",
            "dekurzWho": 0,
            "dekurzDepartment": 0,
        }

        expected = {
            "patient": {
                "external_id": 42,
                "first_name": "John",
                "last_name": "Smith",
                "birth_number": "1234567891",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "123456789",
                "height": 173.0,
                "weight": 61.0,
            },
            "care": {
                "external_id": 43,
                "department": 600,
                "started_at": "2021-12-26 14:27",
                "finished_at": None,
                "main_diagnosis": "U071",
            },
            "dekurz": None,
        }

        output_data = patient_transformer(input_data)

        self.assertEqual(output_data, expected)

    def test_patient_transformer_without_insurance_number(self):
        """
        Patient without insuranceNumber
        should the "birthNumber" as "insuranceNumber".
        """
        input_data = {
            "patientId": 42,
            "name": "Doe John",
            "birthNumber": "1234567890",
            "birthDate": "1987-04-02",
            "insuranceCompany": "111",
            "insuranceNumber": "",
            "height": 173.0,
            "weight": 61.0,
            "diagnosis": "U071",
            "hospitalizationId": 43,
            "departmentIn": 600,
            "dateIn": "2021-12-26 14:27",
            "dekurzTime": "2022-01-06 09:30",
            "dekurzWho": 70331,
            "dekurzDepartment": 600,
        }

        expected = {
            "patient": {
                "external_id": 42,
                "first_name": "John",
                "last_name": "Doe",
                "birth_number": "1234567890",
                "birth_date": "1987-04-02",
                "insurance_company": "111",
                "insurance_number": "1234567890",
                "height": 173.0,
                "weight": 61.0,
            },
            "care": {
                "external_id": 43,
                "department": 600,
                "started_at": "2021-12-26 14:27",
                "finished_at": None,
                "main_diagnosis": "U071",
            },
            "dekurz": {
                "made_at": "2022-01-06 09:30",
                "doctor": 70331,
                "department": 600,
            },
        }

        output_data = patient_transformer(input_data)

        self.assertEqual(output_data, expected)

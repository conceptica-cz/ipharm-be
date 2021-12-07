def patient_transformer(data: dict) -> dict:
    return {
        "patient": {
            "external_id": data["patientId"],
            "first_name": data["firstName"],
            "last_name": data["lastName"],
            "birth_number": data["birthNumber"],
            "birth_date": data["birthDate"],
            "insurance_company": data["insuranceCompany"],
            "insurance_number": data["insuranceNumber"],
            "height": data["height"],
            "weight": data["weight"],
        },
        "care": {
            "external_id": data["recordId"],
            "department": data["departmentIn"],
            "started_at": data["dateIn"],
            "finished_at": data["dateOut"],
            "main_diagnosis": data["diagnosis"],
        },
        "dekurz": {
            "made_at": data["dekurzTime"],
            "doctor": data["dekurzWho"],
            "department": data["dekurzDepartment"],
        },
    }

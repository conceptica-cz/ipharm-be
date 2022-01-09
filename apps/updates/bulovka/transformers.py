def patient_transformer(data: dict) -> dict:
    transformed = {
        "patient": {
            "external_id": data["patientId"],
            "first_name": data["name"].split(" ", 1)[1],
            "last_name": data["name"].split(" ", 1)[0],
            "birth_number": data["birthNumber"],
            "birth_date": data["birthDate"],
            "insurance_company": data["insuranceCompany"],
            "insurance_number": data["insuranceNumber"],
            "height": data["height"],
            "weight": data["weight"],
        },
        "care": {
            "external_id": data.get("hospitalizationId"),
            "department": data["departmentIn"],
            "started_at": data["dateIn"],
            "finished_at": data.get("dateOut"),
            "main_diagnosis": data["diagnosis"],
        },
        "dekurz": None,
    }
    if data.get("dekurzTime"):
        transformed["dekurz"] = {
            "made_at": data["dekurzTime"],
            "doctor": data["dekurzWho"],
            "department": data["dekurzDepartment"],
        }
    return transformed

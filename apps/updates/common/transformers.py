def delete_id(data: dict):
    if "id" in data:
        del data["id"]
    return data


def id_to_reference_id(data: dict):
    data["reference_id"] = data.pop("id")
    return data

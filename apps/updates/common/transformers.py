def delete_id(data: dict):
    if "id" in data:
        del data["id"]
    return data


def temporary(data: dict):
    data["external_id"] = data.pop("identifier")
    return data

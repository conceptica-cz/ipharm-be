def delete_id(data: dict):
    if "id" in data:
        del data["id"]
    return data

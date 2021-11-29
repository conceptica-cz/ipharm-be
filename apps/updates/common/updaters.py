from django.apps import apps


def simple_model_updater(data: dict, **kwargs) -> dict:
    app, model = kwargs["model"].split(".")
    model_class = apps.get_model(app, model)
    _, operation = model_class.objects.update_or_create_from_dict(
        identifiers=kwargs["identifiers"],
        data=data,
        relations=kwargs.get("relations"),
        update=kwargs.get("update"),
    )
    return {kwargs["model"]: operation}

from django.utils import timezone
from updates.models import ModelUpdate, Update


def finish_update(update_results: dict, update_id: int):
    update = Update.objects.get(id=update_id)
    update.finished_at = timezone.now()
    update.save()
    total = {}
    for result in update_results:
        for model, operation in result.items():
            model_result = total.setdefault(model, {})
            model_result[operation] = model_result.get(operation, 0) + 1

    for model, operations in total.items():
        ModelUpdate.objects.create(
            update=update,
            name=model,
            created=operations.get("created", 0),
            updated=operations.get("updated", 0),
            not_changed=operations.get("not_changed", 0),
        )

from django.db import models


class BaseSoftDeletableManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return super().get_queryset().filter(is_deleted=False)
        else:
            return super().get_queryset()

    def hard_delete(self):
        return super().delete()

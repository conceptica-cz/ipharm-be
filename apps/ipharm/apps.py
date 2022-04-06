from django.apps import AppConfig


class IpharmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ipharm"

    def ready(self):
        from . import signals

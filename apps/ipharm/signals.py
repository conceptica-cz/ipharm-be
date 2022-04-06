from django.db.models.signals import m2m_changed
from django.dispatch import receiver


@receiver(m2m_changed)
def save_m2m(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Explicitly save m2m relations to keep history records."""
    if action.startswith("post_"):
        for field in instance._meta.many_to_many:
            if sender == getattr(instance, field.name).through:
                for through_instance in getattr(
                    instance, field.name
                ).through.objects.all():
                    through_instance.save()
                    pass

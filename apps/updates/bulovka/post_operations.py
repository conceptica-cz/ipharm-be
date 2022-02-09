from ipharm.models import Patient


def update_names():
    Patient.objects.update_names()

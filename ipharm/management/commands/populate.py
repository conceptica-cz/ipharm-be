import random

from django.core.management.base import BaseCommand

from factories.ipharm import patients


class Command(BaseCommand):
    help = "Populate database with fake data"

    def handle(self, *args, **options):
        print("Populating database. Please wait...")
        for i in range(800):
            patients.PatientFactory()
        ambulances = [patients.AmbulanceFactory() for i in range(10)]
        for i in range(200):
            patients.PatientFactory(clinic=random.choice(ambulances))

        print("Database was populated.")

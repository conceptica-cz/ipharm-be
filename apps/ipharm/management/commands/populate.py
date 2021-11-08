import random

from django.core.management.base import BaseCommand

from factories.ipharm import patients
from factories.references import clinics


class Command(BaseCommand):
    help = "Populate database with fake data"

    def handle(self, *args, **options):
        print("Populating database. Please wait...")
        for i in range(1800):
            patients.PatientFactory()

        print("Database was populated.")

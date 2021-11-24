import random

from django.core.management.base import BaseCommand

from factories.ipharm import CareFactory
from factories.references import AdverseEffectFactory, IdentificationFactory, TagFactory


class Command(BaseCommand):
    help = "Populate database with fake data"

    def handle(self, *args, **options):
        print("Populating database. Please wait...")
        for i in range(50):
            TagFactory()
            AdverseEffectFactory()
        for i in range(100):
            CareFactory()
        IdentificationFactory()
        print("Database was populated.")

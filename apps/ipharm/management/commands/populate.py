import random

from django.core.management.base import BaseCommand

from factories.ipharm import (
    CareFactory,
    CheckInFactory,
    PatientInformationFactory,
    PharmacologicalEvaluationFactory,
    PharmacologicalPlanCommentFactory,
    PharmacologicalPlanFactory,
    RiskDrugHistoryFactory,
)
from factories.references import (
    AdverseEffectFactory,
    ExternalDepartmentFactory,
    IdentificationFactory,
    TagFactory,
)


class Command(BaseCommand):
    help = "Populate database with fake data"

    def handle(self, *args, **options):
        print("Populating database. Please wait...")
        for i in range(50):
            TagFactory()
            AdverseEffectFactory()
        for i in range(800):
            care = CareFactory()
            if random.randint(0, 1):
                CheckInFactory(care=care)
                if random.randint(0, 1):
                    pharmacological_plan = PharmacologicalPlanFactory(care=care)
                    [
                        PharmacologicalPlanCommentFactory(
                            pharmacological_plan=pharmacological_plan,
                            comment_type="verification",
                        )
                        for _ in range(random.randint(0, 2))
                    ]
                    [
                        PharmacologicalPlanCommentFactory(
                            pharmacological_plan=pharmacological_plan,
                            comment_type="comment",
                        )
                        for _ in range(random.randint(0, 5))
                    ]
                    RiskDrugHistoryFactory(care=care)
                    [
                        PatientInformationFactory(care=care)
                        for _ in range(random.randint(1, 5))
                    ]
                    [
                        PharmacologicalEvaluationFactory(care=care)
                        for _ in range(random.randint(1, 5))
                    ]

        for i in range(30):
            ExternalDepartmentFactory()
        IdentificationFactory()
        print("Database was populated.")

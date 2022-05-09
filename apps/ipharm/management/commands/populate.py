import random

from django.conf import settings
from django.core.management.base import BaseCommand
from ipharm.models.patients import Patient
from references.models import Department

from factories.ipharm import (
    CareFactory,
    CheckInFactory,
    PatientFactory,
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
from factories.users import UserFactory


class Command(BaseCommand):
    help = "Populate database with fake data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            default=False,
            help="Delete existing models.",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            self._delete_models()

        if settings.ENVIRONMENT not in ["test", "development", "local"]:
            self.stdout.write(
                self.style.ERROR(
                    "This command should only be used in test, local or development environments."
                )
            )
            return
        print("Populating database. Please wait...")

        users = [
            UserFactory(),
            UserFactory(),
            UserFactory(),
            UserFactory(),
            UserFactory(),
        ]

        for i in range(50):
            TagFactory()
            AdverseEffectFactory()
        for i in range(101):
            patient = PatientFactory()
            care = CareFactory(last_dekurz__add=True, patient=patient)
            print(f"Patient {patient} created")
            if random.randint(0, 1):
                CheckInFactory(
                    care=care,
                    drugs__add=True,
                    diagnoses__add=True,
                    high_interaction_potential_drugs__add=True,
                    narrow_therapeutic_window_drugs__add=True,
                )
                if random.randint(0, 1):
                    pharmacological_plan = PharmacologicalPlanFactory(
                        care=care,
                        tags__add=True,
                    )
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
                    RiskDrugHistoryFactory(
                        care=care,
                        tags__add=True,
                        diagnoses__add=True,
                    )
                    for _ in range(random.randint(1, 4)):
                        patient_information = PatientInformationFactory(care=care)
                        for i in range(random.randint(1, 4)):
                            patient_information.text = i
                            patient_information.save()
                            patient_information.set_history_user(random.choice(users))

                    [
                        PharmacologicalEvaluationFactory(care=care, tags__add=True)
                        for _ in range(random.randint(1, 5))
                    ]

        for i in range(30):
            ExternalDepartmentFactory()
        department = Department.objects.first()
        department.for_insurance = True
        department.save()
        IdentificationFactory(for_insurance=True)
        print("Database was populated.")

    def _delete_models(self):
        Patient.objects.all().delete()
        print("Models were deleted.")

from django.db import models
from updates.models import BaseUpdatableModel


class Care(BaseUpdatableModel):
    HOSPITALIZATION = "hospitalization"
    AMBULATION = "ambulation"

    CARE_TYPE_CHOICES = (
        (HOSPITALIZATION, "Hospitalization"),
        (AMBULATION, "Ambulation"),
    )
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    diagnoses = models.ManyToManyField("references.Diagnosis", through="CareDiagnosis")
    care_type = models.CharField(
        max_length=20, choices=CARE_TYPE_CHOICES, default=HOSPITALIZATION
    )
    is_active = models.BooleanField(default=True)
    external_id = models.CharField("UNIS ID", max_length=50, null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    clinic = models.ForeignKey(
        "references.Clinic", on_delete=models.CASCADE, null=True, blank=True
    )
    department = models.ForeignKey(
        "references.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients",
    )
    dekurzes = models.ManyToManyField("Dekurz", related_name="dekurz_cares")
    last_dekurz = models.ForeignKey(
        "Dekurz",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="last_dekurz_care",
    )

    def update_diagnoses(self, diagnosis) -> None:
        """
        Update diagnoses, but keep diagnosis received via api

        :param diagnosis: list of `Diagnosis` objects
        """
        current_ids = self.diagnoses.values_list("id", flat=True)
        via_api_ids = [d.id for d in self.diagnoses.filter(carediagnosis__via_api=True)]
        ids_to_keep = [d.id for d in diagnosis] + via_api_ids
        self.diagnoses.exclude(id__in=ids_to_keep).delete()
        for diagnosis in set(filter(lambda d: d.id not in current_ids, diagnosis)):
            self.carediagnosis_set.create(care=self, diagnosis=diagnosis)

    def add_dekurz(self, dekurz):
        self.dekurzes.add(dekurz)
        self.last_dekurz = dekurz
        self.save()

    def __str__(self):
        return f"Care {self.id} - {self.patient} - {self.care_type}"


class Dekurz(BaseUpdatableModel):
    care = models.ForeignKey("Care", on_delete=models.CASCADE)
    made_at = models.DateTimeField(null=True, blank=True)
    doctor = models.ForeignKey(
        "references.Person", on_delete=models.SET_NULL, null=True, blank=True
    )
    department = models.ForeignKey(
        "references.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients_dekurz",
    )


class CareDiagnosis(BaseUpdatableModel):
    care = models.ForeignKey("Care", on_delete=models.CASCADE)
    diagnosis = models.ForeignKey("references.Diagnosis", on_delete=models.CASCADE)
    via_api = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.care} {self.diagnosis}"

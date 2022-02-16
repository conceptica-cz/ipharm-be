import os
from io import BytesIO, StringIO

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from references.models import InsuranceCompany
from reports.generic_report import GenericReportFactory
from updates.models import BaseUpdatableModel

DOSAGE_PREFIX = "KDAVKA"


def insurance_upload_to(instance, filename):
    """
    Upload file to the right path
    """
    return f"{settings.INSURANCE_REPORT_FOLDER}/{instance.year}/{instance.month}/{filename}"


class InsuranceReport(BaseUpdatableModel):
    """
    Insurance report model
    """

    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE)
    documents_number = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    data = models.JSONField(default=dict)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=insurance_upload_to)

    def save_file(self):
        file = StringIO(self.content)
        filename = f"{DOSAGE_PREFIX}.{self.insurance_company.code}"
        self.file.save(filename, file)


class GenericReportType(models.Model):
    """
    Generic report type model
    """

    FREQUENCY_MONTHLY = "monthly"
    FREQUENCY_YEARLY = "yearly"

    FREQUENCY_CHOICES = (
        (FREQUENCY_MONTHLY, "Monthly"),
        (FREQUENCY_YEARLY, "Yearly"),
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)
    file_name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    frequency = models.CharField(
        max_length=255, choices=FREQUENCY_CHOICES, default=FREQUENCY_MONTHLY
    )
    formats = ArrayField(models.CharField(max_length=255), default=list)

    def __str__(self):
        return self.name

    def generate_report(
        self, report_format: str = "pdf", year=None, month=None, **kwargs
    ) -> "GenericReportFile":
        if report_format not in self.formats:
            raise ValueError(f"{report_format} is not supported")

        if year is None:
            year = timezone.now().year
        if month is None:
            month = timezone.now().month

        if self.frequency == self.FREQUENCY_MONTHLY:
            generic_report_file, _ = GenericReportFile.objects.update_or_create(
                report_type=self,
                year=year,
                month=month,
                report_format=report_format,
            )
        else:
            generic_report_file, _ = GenericReportFile.objects.update_or_create(
                report_type=self,
                year=year,
                report_format=report_format,
                defaults={
                    "month": None,
                },
            )

        generic_report = GenericReportFactory().create(
            report_name=self.name,
            report_format=report_format,
            **{"year": year, "month": month} | kwargs,
        )

        content = generic_report.render()

        generic_report_file.save_file(content)
        return generic_report_file


def generic_upload_to(instance, filename):
    """
    Upload file to the right path
    """
    postfix = ""
    if instance.report_type.frequency == GenericReportType.FREQUENCY_MONTHLY:
        if instance.month < 10:
            postfix = f"_{instance.year}_0{instance.month}"
        else:
            postfix = f"_{instance.year}_{instance.month}"
    elif instance.report_type.frequency == GenericReportType.FREQUENCY_YEARLY:
        postfix = f"_{instance.year}"

    report_path = (
        f"{settings.GENERIC_REPORT_FOLDER}/{filename}{postfix}.{instance.report_format}"
    )
    system_path = f"{settings.MEDIA_ROOT}/{report_path}"
    if os.path.exists(system_path):
        os.remove(system_path)
    return report_path


class GenericReportFile(BaseUpdatableModel):
    report_type = models.ForeignKey(GenericReportType, on_delete=models.CASCADE)
    file = models.FileField(upload_to=generic_upload_to)
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    report_format = models.CharField(max_length=255, default="pdf")

    def save_file(self, content: str):
        if isinstance(content, bytes):
            file = BytesIO(content)
        else:
            file = StringIO(content)
        filename = f"{self.report_type.file_name}"
        self.file.save(filename, file)

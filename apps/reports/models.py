from io import BytesIO, StringIO

from django.db import models
from references.models import InsuranceCompany
from updates.models import BaseUpdatableModel

DOSAGE_PREFIX = "KDAVKA"

# def upload_to(instance, filename):
#     """
#     Upload file to the right path
#     """
#     return f"reports/{instance.id}/{filename}"
#
#
# class FileAlreadyExists(Exception):
#     pass
#
#
# class ReportFile(models.Model):
#     """
#     Report model
#     """
#
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     file = models.FileField(upload_to=upload_to)
#
#     def file_from_string(self, content: str):
#         """Generate a file from a string"""
#         if self.file:
#             raise FileAlreadyExists(self.file.name)
#         file = StringIO(content)
#         self.file.save(self.name, file)
#
#     def __str__(self):
#         return self.name


def insurance_upload_to(instance, filename):
    """
    Upload file to the right path
    """
    return f"dosages/{instance.year}/{instance.month}/{filename}"


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

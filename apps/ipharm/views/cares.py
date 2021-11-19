from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from ..models import Care
from ..models.patients import Patient
from ..serializers.cares import CareNestedSerializer, CareSerializer


class CareDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Care.objects.all()
    serializer_class = CareNestedSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CareNestedSerializer
        else:
            return CareSerializer


class PatientCareDetailView(generics.GenericAPIView, CreateModelMixin):
    queryset = Care.objects.all()

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            kwargs["data"] = kwargs["data"].copy()
            kwargs["data"]["patient"] = self.patient.pk
            if self.kwargs["care_type"] == "hospital":
                kwargs["data"]["care_type"] = Care.HOSPITALIZATION
            else:
                kwargs["data"]["care_type"] = Care.AMBULATION
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CareNestedSerializer
        else:
            return CareSerializer

    def post(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=self.kwargs["patient_pk"])
        if (
            self.kwargs["care_type"] == "hospital"
            and self.patient.current_hospital_care
            or self.kwargs["care_type"] == "ambulance"
            and self.patient.current_ambulance_care
        ):
            return Response(
                {
                    "detail": "Patient already has a care",
                    "code": "patient_already_has_care",
                },
                status=status.HTTP_409_CONFLICT,
            )
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        care = serializer.save()
        self.patient.set_current_care(care)

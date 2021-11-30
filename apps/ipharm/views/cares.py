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

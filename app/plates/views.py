from plates.models import BeadPlate, Plate, Run
from plates.serializers import BeadPlateSerializer, PlateSerializer, RunSerializer
from django.http import Http404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BeadPlateList(APIView):
    """List all BeadPlates"""

    def get(self, request, format=None):
        bead_plates = (
            BeadPlate.objects.all()
        )
        serializer = BeadPlateSerializer(bead_plates, many=True)
        return Response(serializer.data)


class PlateList(APIView):
    """List all Plates"""

    def get(self, request, format=None):
        plates = (
            Plate.objects.all()
        )
        serializer = PlateSerializer(plates, many=True)
        return Response(serializer.data)


class RunList(APIView):
    """List all Runs"""

    def get(self, request, format=None):
        runs = (
            Run.objects.all()
        )
        serializer = RunSerializer(runs, many=True)
        return Response(serializer.data)


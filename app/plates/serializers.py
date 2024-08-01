from re import search
from rest_framework import serializers
from plates.models import BeadPlate, Plate, Run


class BeadPlateSerializer(serializers.ModelSerializer):
    """Serializer for a BeadPlate object"""

    class Meta:
        model = BeadPlate
        fields = ["id", "name"]


class PlateSerializer(serializers.ModelSerializer):
    """Serializer for a BeadPlate object"""

    class Meta:
        model = Plate
        fields = ["id", "name", "is_cali"]


class RunSerializer(serializers.ModelSerializer):
    """Serializer for a BeadPlate object"""

    class Meta:
        model = Run
        fields = ["id", "nel_id", "date"]


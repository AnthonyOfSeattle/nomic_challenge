from plates.models import BeadPlate, Plate, Run
from plates.serializers import BeadPlateSerializer, PlateSerializer, RunSerializer
from django.db import connection
from django.http import Http404
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


class BeadPlateList(APIView):
    """List all BeadPlates"""

    def get(self, request, format=None):
        # Get parameters from request
        return_data = request.GET.get("return_data", "true")

        # Query for plates
        bead_plates = (
            BeadPlate.objects.all()
        )

        # Return count and records
        response = {"count": bead_plates.count()}
        if return_data.lower() != "false":
            serializer = BeadPlateSerializer(bead_plates, many=True)
            response["data"] = serializer.data

        return Response(response)


class PlateList(APIView):
    """List all Plates"""

    def get(self, request, format=None):
        # Get parameters from request
        run_date_gt = request.GET.get("run_date_gt")
        run_date_lt = request.GET.get("run_date_lt")
        return_data = request.GET.get("return_data", "true")

        # Query for plates
        plates = Plate.objects.all()
        if run_date_gt:
            plates = plates.filter(run__date__gt=run_date_gt)

        if run_date_lt:
            plates = plates.filter(run__date__lt=run_date_lt)

        # Return count and records
        response = {"count": plates.count()}
        if return_data.lower() != "false":
            serializer = PlateSerializer(plates, many=True)
            response["data"] = serializer.data

        return Response(response)


class RunList(APIView):
    """List all Runs"""

    def get(self, request, format=None):
        # Get parameters from request
        date_gt = request.GET.get("date_gt")
        date_lt = request.GET.get("date_lt")
        return_data = request.GET.get("return_data", "true")

        # Query for runs
        runs = Run.objects.all()
        if date_gt:
            runs = runs.filter(date__gt=date_gt)

        if date_lt:
            runs = runs.filter(date__lt=date_lt)

        # Return count and records
        response = {"count": runs.count()}
        if return_data.lower() != "false":
            serializer = RunSerializer(runs, many=True)
            response["data"] = serializer.data

        return Response(response)


@api_view(["GET"])
def plate_report(request):
    """
    Generate report of number of plates ran

    This function uses a raw query to postgres since the logic is 10 times cleaner.
    Ultimately this is the most performant option too.
    """

    query = """
    SELECT DATE_TRUNC('month', date) as month, count(*)
    FROM plates_run, plates_plate
    WHERE plates_run.id = plates_plate.run_id
    GROUP BY month
    ORDER BY month
    """
    cursor = connection.cursor()
    cursor.execute(query)

    response = []
    for (datetime, count) in cursor.fetchall():
        response.append(
            {
                "month": datetime,
                "count": count 
            }
        )

    return Response(response)


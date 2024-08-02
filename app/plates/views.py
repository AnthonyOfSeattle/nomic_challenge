from time import sleep
from plates.models import BeadPlate, Plate, Run
from plates.serializers import BeadPlateSerializer, PlateSerializer, RunSerializer
from plates.tasks import count_occurences_below_threshold, get_calimetrics
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

        bead_count_threshold = request.GET.get("bead_count_threshold")
        occurence_threshold = request.GET.get("occurence_threshold")

        # Query for plates
        plates = Plate.objects.all()
        if run_date_gt:
            plates = plates.filter(run__date__gt=run_date_gt)

        if run_date_lt:
            plates = plates.filter(run__date__lt=run_date_lt)

        # Perform filtering based on count threshold
        count_dict = {}
        if bead_count_threshold and occurence_threshold:
            async_results = [
                count_occurences_below_threshold.delay(plate.name, int(bead_count_threshold))
                for plate in plates
            ]
            while any([not result.ready() for result in async_results]):
                sleep(1)

            count_dict = {
                entry.get()["plate_name"] : entry.get()["count"]
                for entry in async_results
            }
            plates = plates.filter(
                name__in=[
                    name for name, count in count_dict.items()
                    if count > int(occurence_threshold)
                ]
            )

        # Return count and records
        response = {"count": plates.count()}
        if return_data.lower() != "false":
            serializer = PlateSerializer(plates, many=True)
            response["data"] = [
                {
                    **entry,
                    **(
                        {"counts_below_threshold": count_dict[entry["name"]]}
                        if entry["name"] in count_dict else {}
                    )
                }
                for entry in serializer.data
            ]

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
def get_plate_report(request):
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

@api_view(["GET"])
def get_calimetrics_list(request):
    """
    Generate report of number of plates ran
    """
    
    # Get parameters from request
    return_discrepency = request.GET.get("return_discrepency", False)

    # Get Caliplates
    plates = Plate.objects.filter(is_cali=True)

    # Get calidata async
    async_results = [
        get_calimetrics.delay(plate.name, return_discrepency)
        for plate in plates
    ]
    while any([not result.ready() for result in async_results]):
        sleep(1)

    data = [result.get() for result in async_results]
    data = [
        entry for entry in data
        if not return_discrepency or entry["calimetrics"]
    ]
    return Response({"count": len(data), "data": data})

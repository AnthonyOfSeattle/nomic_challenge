from plates.models import Plate
from plates.utils import get_s3_bucket, load_s3_object
from celery import shared_task


@shared_task
def count_occurences_below_threshold(plate_name, threshold):
    s3_bucket = get_s3_bucket()
    s3_objects = list(
        s3_bucket.objects.filter(
            Prefix=f"DecodingResults/{plate_name}/bead_counts.csv"
        )
    )
    if not s3_objects:
        return

    data = load_s3_object(s3_objects[0])
    occurences_below = int((
        (data < threshold).sum()
    ).sum())

    return {"plate_name": plate_name, "count": occurences_below}


@shared_task
def get_calimetrics(plate_name, return_discrepency=True, threshold=2):
    s3_bucket = get_s3_bucket()

    # Load reported calimetrics
    s3_objects = list(
        s3_bucket.objects.filter(
            Prefix=f"CALIMetrics/{plate_name}/metrics.csv"
        )
    )
    if not s3_objects:
        return

    calimetrics = load_s3_object(s3_objects[0])
    calimetrics = {
        sensor: float(value)
        for sensor, value in calimetrics.to_records()
    }
    
    # Load re-calculated calimetrics
    if return_discrepency:
        s3_objects = list(
            s3_bucket.objects.filter(
                Prefix=f"DecodingResults/{plate_name}/bead_counts.csv"
            )
        )
        if not s3_objects:
            return

        data = load_s3_object(s3_objects[0])
        recalculated_calimetrics = {
                sensor: float(value)
                for sensor, value in data.mean().to_frame().to_records()
        }

    # Build results
    data = []
    for sensor, value in calimetrics.items():
        if return_discrepency:
            deviation = abs(value - recalculated_calimetrics[sensor])
            if deviation <= threshold:
                continue

            data.append(
                {"sensor": sensor, "value": value, "deviation": deviation}
            )

        else:
            data.append(
                {"sensor": sensor, "value": value}
            )
    
    return {"plate_name": plate_name, "calimetrics": data}

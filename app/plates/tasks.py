from plates.models import Plate
from plates.utils import get_s3_bucket, load_s3_object
from celery import shared_task


@shared_task
def count_occurences_below_threshold(plate_name, threshold):
    """"""
    plate = Plate.objects.filter(name=plate_name)[0]
    s3_bucket = get_s3_bucket()
    s3_objects = list(
        s3_bucket.objects.filter(
            Prefix=f"DecodingResults/{plate.name}/bead_counts.csv"
        )
    )
    if not s3_objects:
        return

    data = load_s3_object(s3_objects[0])
    occurences_below = int((
        (data < threshold).sum()
    ).sum())

    return {"plate_name": plate_name, "count": occurences_below} 

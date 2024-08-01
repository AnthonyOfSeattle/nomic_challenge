import os
import sys
from itertools import groupby
from plates.models import BeadPlate, Plate, Run
from plates.utils import get_s3_bucket, load_s3_object
from django.core.management.base import BaseCommand


def load_beadplates_metadata(metadata):
    beadplate_names = [entry["name"] for entry in metadata]
    matching_beadplates = {
        entry.name for entry in BeadPlate.objects.filter(name__in=beadplate_names)
    }

    for entry in metadata:
        if entry["name"] in matching_beadplates:
            continue

        BeadPlate(name=entry["name"]).save()
        matching_beadplates.add(entry["name"])
    

def load_run_metadata(metadata):
    run_nel_ids = [entry["nel_id"] for entry in metadata]
    matching_runs = {
        entry.nel_id for entry in Run.objects.filter(nel_id__in=run_nel_ids)
    }

    for entry in metadata:
        if entry["nel_id"] in matching_runs:
            continue

        # If no timezone, interpret as UTC
        date = entry["date"]
        if "+" not in date:
            date += "Z"

        Run(nel_id=entry["nel_id"], date=date).save()
        matching_runs.add(entry["nel_id"])


def load_plate_metadata(metadata):
    plate_names = [entry["name"] for entry in metadata]
    matching_plates = {
        entry.name for entry in Plate.objects.filter(name__in=plate_names)
    }

    for (bead_plate, run), group in groupby(metadata, key=lambda x: (x["beadplate"], x["run"])):
        bead_plate = BeadPlate.objects.filter(name=bead_plate)[0]
        run = Run.objects.filter(nel_id=run)[0]
        for entry in group:
            if entry["name"] in matching_plates:
                continue

            Plate(
                name=entry["name"],
                is_cali=entry["is_cali"],
                bead_plate=bead_plate,
                run=run
            ).save()
            matching_plates.add(entry["name"])



def load_metadata(s3_object):
    metadata = load_s3_object(s3_object)

    load_beadplates_metadata(metadata.get("beadplates", []))
    load_run_metadata(metadata.get("runs", []))
    load_plate_metadata(metadata.get("plates", []))


class Command(BaseCommand):
    help = "Downloads metadata for plates"

    def handle(self, *args, **options):
        s3_bucket = get_s3_bucket()
        for s3_object in s3_bucket.objects.filter(Prefix="metadata"):
            if s3_object.key.endswith("metadata.json"):
                load_metadata(s3_object)


        #plate_metadata = [
        #    load_s3_object(o)
        #    for o in s3_bucket.objects.all()
        #    if o.key.startswith("metadata")
        #]

        

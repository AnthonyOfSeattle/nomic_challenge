from django.db import models
from django.contrib.sessions.models import Session


class BeadPlate(models.Model):
    """Model to store individual BeadPlates"""

    name = models.CharField(max_length=50)

    def __str__(self):
        return f"BeadPlate('{self.name}')"


class Run(models.Model):
    """Model to store individual Runs"""

    nel_id = models.CharField(max_length=50)
    date = models.DateTimeField()

    def __str__(self):
        return f"Run('{self.nel_id}', {self.date})"


class Plate(models.Model):
    """Model to store individual Plates"""

    # Notes: Why is "name" a char field?
    # Even though the Plate Names are integers
    # I saw that BeadPlates and Runs include IDs with
    # non-numeric characters. In real life, I would
    # ask the instrument operators whether making this
    # an integer field was ok.
    name = models.CharField(max_length=50)
    is_cali = models.BooleanField()

    # Links to other entities
    bead_plate = models.ForeignKey(BeadPlate,
                                   related_name='plates',
                                   on_delete=models.CASCADE)
    run = models.ForeignKey(Run,
                            related_name='plates',
                            on_delete=models.CASCADE)

    def __str__(self):
        return f"Plate('{self.id}', is_cali={self.is_cali})"


class AnalysisResult(models.Model):
    """Model to store AnalysisResult linkages"""
    cali_plate = models.ForeignKey(Plate,
                                   related_name='calibrates_results',
                                   null=True,
                                   on_delete=models.SET_NULL)
    sample_plates = models.ManyToManyField(Plate, related_name='results')

from django.contrib import admin
from plates.models import AnalysisResult, BeadPlate, Plate, Run


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    pass


@admin.register(BeadPlate)
class BeadPlateAdmin(admin.ModelAdmin):
    pass


@admin.register(Plate)
class PlateAdmin(admin.ModelAdmin):
    pass


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    pass


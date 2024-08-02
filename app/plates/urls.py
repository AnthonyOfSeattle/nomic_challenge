from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from plates import views

urlpatterns = [
    path("bead_plates/", views.BeadPlateList.as_view()),
    path("plates/", views.PlateList.as_view()),
    path("plates/report/", views.get_plate_report),
    path("runs/", views.RunList.as_view()),
    path("calimetrics/", views.get_calimetrics_list)
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from plates import views

urlpatterns = [
    path("bead_plates/", views.BeadPlateList.as_view()),
    path("plates/", views.PlateList.as_view()),
    path("runs/", views.RunList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

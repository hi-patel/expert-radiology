from django.urls import path

from apps.imaging_centers.views import ImagingCenterListView

urlpatterns = [
    path("", ImagingCenterListView.as_view(), name="imaging-center-list"),
]


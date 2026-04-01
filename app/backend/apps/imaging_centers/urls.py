from django.urls import path

from apps.imaging_centers.views import (
    ImagingCenterSearchView,
    InsurancePlanListView,
    ModalityListView,
)

urlpatterns = [
    path("imaging-centers/", ImagingCenterSearchView.as_view(), name="imaging-center-search"),
    path("modalities/", ModalityListView.as_view(), name="modality-list"),
    path("insurance-plans/", InsurancePlanListView.as_view(), name="insurance-plan-list"),
]

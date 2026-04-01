from django.db.models import Q
from rest_framework import generics

from apps.imaging_centers.models import ImagingCenter
from apps.imaging_centers.serializers import ImagingCenterSerializer


class ImagingCenterListView(generics.ListAPIView):
    serializer_class = ImagingCenterSerializer

    def get_queryset(self):
        queryset = ImagingCenter.objects.all().prefetch_related("modalities", "insurance_plans")

        rating_min = self.request.query_params.get("rating_min")
        if rating_min is not None:
            queryset = queryset.filter(patient_satisfaction_rating__gte=rating_min)

        modality_id = self.request.query_params.get("modality_id")
        if modality_id is not None:
            queryset = queryset.filter(modalities__id=modality_id)

        insurance_plan_id = self.request.query_params.get("insurance_plan_id")
        if insurance_plan_id is not None:
            queryset = queryset.filter(insurance_plans__id=insurance_plan_id)

        requires_referral_bonus = self.request.query_params.get("requires_referral_bonus")
        if requires_referral_bonus in {"1", "true", "True"}:
            queryset = queryset.filter(referral_bonus_amount__isnull=False)

        sort = self.request.query_params.get("sort")
        if sort == "distance_from_patient":
            # Placeholder: distance calculations will require geospatial data; for now, no-op ordering.
            queryset = queryset.order_by("id")
        elif sort == "patient_satisfaction_desc":
            queryset = queryset.order_by("-patient_satisfaction_rating")
        elif sort == "referral_bonus_desc":
            queryset = queryset.order_by("-referral_bonus_amount")
        elif sort == "turnaround_time_asc":
            queryset = queryset.order_by("average_turnaround_hours")

        return queryset.distinct()

from django.shortcuts import render

# Create your views here.

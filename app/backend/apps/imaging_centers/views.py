from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.imaging_centers.models import ImagingCenter
from apps.imaging_centers.serializers import (
    ImagingCenterSerializer,
    InsurancePlanSerializer,
    ModalitySerializer,
)
from apps.insurance.models import InsurancePlan
from apps.radiology.models import Modality


def _haversine_km(
    lat1: Optional[float],
    lon1: Optional[float],
    lat2: Optional[float],
    lon2: Optional[float],
) -> Optional[float]:
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return None

    r = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


@dataclass
class SortSpec:
    key: str
    direction: str  # "asc" or "desc"


class ImagingCenterSearchView(APIView):
    """
    Search endpoint backing the physician UI.

    Expects a JSON body with:
    - patient_address (required string, used for display only for now)
    - target_address (optional string)
    - patient_lat, patient_lng (optional, used for distance calculations)
    - target_lat, target_lng (optional)
    - modality_ids: list[int]
    - insurance_plan_ids: list[int]
    - minimum_rating: float (e.g. 4.0)
    - requires_referral_bonus: bool
    - minimum_public_transit_score: int
    - sort: list[str] of:
        ["distance_from_patient_asc", "distance_from_target_asc",
         "patient_satisfaction_desc", "turnaround_time_asc",
         "referral_bonus_desc"]
    """

    def post(self, request: Request) -> Response:
        payload = request.data

        try:
            patient_lat = self._to_float(payload.get("patient_lat"))
            patient_lng = self._to_float(payload.get("patient_lng"))
            target_lat = self._to_float(payload.get("target_lat"))
            target_lng = self._to_float(payload.get("target_lng"))
        except (TypeError, ValueError):
            return Response({"detail": "Invalid coordinate values."}, status=status.HTTP_400_BAD_REQUEST)

        modality_ids: Sequence[int] = payload.get("modality_ids", []) or []
        insurance_plan_ids: Sequence[int] = payload.get("insurance_plan_ids", []) or []
        minimum_rating = self._to_float(payload.get("minimum_rating"))
        requires_referral_bonus = bool(payload.get("requires_referral_bonus", False))
        min_public_transit_score = self._to_int(payload.get("minimum_public_transit_score"))
        sort_spec = self._parse_sort(payload.get("sort", []))

        queryset = ImagingCenter.objects.all().prefetch_related("modalities", "insurance_plans")

        if minimum_rating is not None:
            queryset = queryset.filter(patient_satisfaction_rating__gte=minimum_rating)

        for modality_id in modality_ids:
            queryset = queryset.filter(modalities__id=modality_id)

        if insurance_plan_ids:
            queryset = queryset.filter(insurance_plans__id__in=list(insurance_plan_ids))

        if requires_referral_bonus:
            queryset = queryset.filter(referral_bonus_amount__isnull=False)

        if min_public_transit_score is not None:
            queryset = queryset.filter(public_transit_score__gte=min_public_transit_score)

        centers: List[ImagingCenter] = list(queryset.distinct())

        for center in centers:
            center.distance_from_patient_km = _haversine_km(
                patient_lat,
                patient_lng,
                float(center.latitude) if center.latitude is not None else None,
                float(center.longitude) if center.longitude is not None else None,
            )
            center.distance_from_target_km = _haversine_km(
                target_lat,
                target_lng,
                float(center.latitude) if center.latitude is not None else None,
                float(center.longitude) if center.longitude is not None else None,
            )

        centers = self._apply_sort(centers, sort_spec)

        serializer = ImagingCenterSerializer(centers, many=True)
        return Response(serializer.data)

    def _parse_sort(self, raw: Iterable[str]) -> List[SortSpec]:
        valid_prefixes = {
            "distance_from_patient": "distance_from_patient_km",
            "distance_from_target": "distance_from_target_km",
            "patient_satisfaction": "patient_satisfaction_rating",
            "turnaround_time": "average_turnaround_hours",
            "referral_bonus": "referral_bonus_amount",
        }
        specs: List[SortSpec] = []
        for item in raw:
            if not isinstance(item, str):
                continue
            if item.endswith("_asc"):
                prefix = item[: -len("_asc")]
                direction = "asc"
            elif item.endswith("_desc"):
                prefix = item[: -len("_desc")]
                direction = "desc"
            else:
                continue
            key = valid_prefixes.get(prefix)
            if key is None:
                continue
            specs.append(SortSpec(key=key, direction=direction))
        return specs

    def _apply_sort(self, centers: List[ImagingCenter], specs: List[SortSpec]) -> List[ImagingCenter]:
        def value(center: ImagingCenter, field: str) -> Optional[float]:
            v = getattr(center, field, None)
            if v is None:
                return None
            try:
                return float(v)
            except (TypeError, ValueError):
                return None

        for spec in reversed(specs):
            reverse = spec.direction == "desc"
            centers.sort(
                key=lambda c, f=spec.key: (value(c, f) is None, value(c, f) or 0.0),
                reverse=reverse,
            )
        return centers

    def _to_float(self, raw: object) -> Optional[float]:
        if raw in (None, "", []):
            return None
        return float(raw)

    def _to_int(self, raw: object) -> Optional[int]:
        if raw in (None, "", []):
            return None
        return int(raw)


class ModalityListView(generics.ListAPIView):
    serializer_class = ModalitySerializer
    queryset = Modality.objects.all().order_by("name")


class InsurancePlanListView(generics.ListAPIView):
    serializer_class = InsurancePlanSerializer
    queryset = InsurancePlan.objects.all().order_by("name")


from __future__ import annotations

import random
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, List, TypedDict

from django.db import transaction

from apps.imaging_centers.models import ImagingCenter
from apps.insurance.models import InsurancePlan
from apps.radiology.models import Modality


class VendorImagingCenterPayload(TypedDict):
    id: str
    name: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    postal_code: str
    latitude: float | None
    longitude: float | None
    patient_satisfaction_rating: float
    review_count: int
    average_turnaround_hours: int
    patients_previously_referred: int
    public_transit_score: int | None
    referral_bonus_amount: float | None
    modality_names: List[str]
    insurance_plan_names: List[str]


@dataclass
class ImagingCenterImportResult:
    created_count: int
    updated_count: int


class ImagingCenterImportService:
    """
    Helper for seeding the ImagingCenter table with realistic mock data.

    The data is shaped like a third‑party vendor API response so that we can
    later swap this implementation with a real HTTP client without changing
    the rest of the code.
    """

    def __init__(self, *, total_centers: int = 1000) -> None:
        self.total_centers = total_centers

    def import_mock_data(self) -> ImagingCenterImportResult:
        """
        Generate a mock vendor payload and upsert ImagingCenter rows from it.
        """
        payload = list(self._build_mock_vendor_payload())
        return self._import_from_vendor_payload(payload)

    def _import_from_vendor_payload(
        self, payload: Iterable[VendorImagingCenterPayload]
    ) -> ImagingCenterImportResult:
        created = 0
        updated = 0

        # Preload lookup tables so we do not hit the database repeatedly.
        modalities_by_name = {m.name: m for m in Modality.objects.all()}
        plans_by_name = {p.name: p for p in InsurancePlan.objects.all()}

        centers_to_create: list[ImagingCenter] = []
        existing_by_name: dict[str, ImagingCenter] = {
            c.name: c for c in ImagingCenter.objects.all()
        }

        for item in payload:
            center = existing_by_name.get(item["name"])
            if center is None:
                center = ImagingCenter(
                    name=item["name"],
                    address_line_1=item["address_line_1"],
                    address_line_2=item["address_line_2"],
                    city=item["city"],
                    state=item["state"],
                    postal_code=item["postal_code"],
                    latitude=item["latitude"],
                    longitude=item["longitude"],
                    patient_satisfaction_rating=item["patient_satisfaction_rating"],
                    review_count=item["review_count"],
                    referral_bonus_amount=(
                        Decimal(str(item["referral_bonus_amount"]))
                        if item["referral_bonus_amount"] is not None
                        else None
                    ),
                    average_turnaround_hours=item["average_turnaround_hours"],
                    patients_previously_referred=item["patients_previously_referred"],
                    public_transit_score=item["public_transit_score"],
                )
                centers_to_create.append(center)
                created += 1
                existing_by_name[item["name"]] = center
            else:
                center.address_line_1 = item["address_line_1"]
                center.address_line_2 = item["address_line_2"]
                center.city = item["city"]
                center.state = item["state"]
                center.postal_code = item["postal_code"]
                center.latitude = item["latitude"]
                center.longitude = item["longitude"]
                center.patient_satisfaction_rating = item["patient_satisfaction_rating"]
                center.review_count = item["review_count"]
                center.referral_bonus_amount = (
                    Decimal(str(item["referral_bonus_amount"]))
                    if item["referral_bonus_amount"] is not None
                    else None
                )
                center.average_turnaround_hours = item["average_turnaround_hours"]
                center.patients_previously_referred = item[
                    "patients_previously_referred"
                ]
                center.public_transit_score = item["public_transit_score"]
                center.save(update_fields=[  # type: ignore[call-arg]
                    "address_line_1",
                    "address_line_2",
                    "city",
                    "state",
                    "postal_code",
                    "latitude",
                    "longitude",
                    "patient_satisfaction_rating",
                    "review_count",
                    "referral_bonus_amount",
                    "average_turnaround_hours",
                    "patients_previously_referred",
                    "public_transit_score",
                ])
                updated += 1

        with transaction.atomic():
            if centers_to_create:
                ImagingCenter.objects.bulk_create(centers_to_create)

            # Now that all centers exist and have primary keys, attach M2M data.
            for item in payload:
                center = ImagingCenter.objects.get(name=item["name"])
                center_modalities = [
                    modalities_by_name[name]
                    for name in item["modality_names"]
                    if name in modalities_by_name
                ]
                center_plans = [
                    plans_by_name[name]
                    for name in item["insurance_plan_names"]
                    if name in plans_by_name
                ]
                if center_modalities:
                    center.modalities.set(center_modalities)
                if center_plans:
                    center.insurance_plans.set(center_plans)

        return ImagingCenterImportResult(created_count=created, updated_count=updated)

    def _build_mock_vendor_payload(self) -> Iterable[VendorImagingCenterPayload]:
        """
        Pretend to call a vendor API and return a list of JSON‑serialisable
        records. For now we synthesise realistic‑looking U.S. imaging centers.
        """
        cities = [
            ("San Francisco", "CA", "94103", 37.773972, -122.431297),
            ("Los Angeles", "CA", "90012", 34.052235, -118.243683),
            ("New York", "NY", "10001", 40.712776, -74.005974),
            ("Chicago", "IL", "60601", 41.878113, -87.629799),
            ("Houston", "TX", "77002", 29.760427, -95.369804),
            ("Seattle", "WA", "98101", 47.606209, -122.332069),
            ("Boston", "MA", "02108", 42.360082, -71.05888),
            ("Atlanta", "GA", "30303", 33.749, -84.388),
            ("Miami", "FL", "33130", 25.761681, -80.191788),
            ("Denver", "CO", "80202", 39.739236, -104.990251),
        ]

        street_names = [
            "Market St",
            "Broadway",
            "Main St",
            "Elm St",
            "Pine St",
            "Oak Ave",
            "Cedar Blvd",
            "Maple Ave",
            "Lakeview Dr",
            "Sunset Blvd",
        ]
        suite_prefixes = ["Suite", "Floor", "Unit", "Ste."]

        for idx in range(1, self.total_centers + 1):
            city, state, postal_code, base_lat, base_lng = random.choice(cities)
            street = random.choice(street_names)
            street_number = random.randint(10, 9999)

            address_line_1 = f"{street_number} {street}"
            address_line_2 = (
                f"{random.choice(suite_prefixes)} {random.randint(100, 1900)}"
                if random.random() < 0.6
                else ""
            )

            # Slight jitter around a base city centroid.
            latitude = round(base_lat + random.uniform(-0.05, 0.05), 6)
            longitude = round(base_lng + random.uniform(-0.05, 0.05), 6)

            rating = round(random.uniform(3.2, 4.9), 1)
            review_count = random.randint(5, 750)
            avg_turnaround = random.randint(4, 72)
            previously_referred = random.randint(0, 5000)
            transit_score = (
                random.randint(40, 100) if random.random() < 0.7 else None
            )

            # Roughly one third of centers offer a referral bonus so that the
            # UI workflows around incentives have realistic data to exercise.
            if random.random() < 0.33:
                referral_bonus_amount: float | None = round(
                    random.uniform(25, 250), 2
                )
            else:
                referral_bonus_amount = None

            modality_names = self._sample_existing_modality_names()
            insurance_plan_names = self._sample_existing_insurance_plan_names()

            yield VendorImagingCenterPayload(
                id=f"vendor-{idx}",
                name=f"{city} Advanced Imaging Center {idx}",
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                postal_code=postal_code,
                latitude=latitude,
                longitude=longitude,
                patient_satisfaction_rating=rating,
                review_count=review_count,
                average_turnaround_hours=avg_turnaround,
                patients_previously_referred=previously_referred,
                public_transit_score=transit_score,
                referral_bonus_amount=referral_bonus_amount,
                modality_names=modality_names,
                insurance_plan_names=insurance_plan_names,
            )

    def _sample_existing_modality_names(self) -> list[str]:
        all_names = list(Modality.objects.values_list("name", flat=True))
        if not all_names:
            return []
        sample_size = random.randint(1, min(5, len(all_names)))
        return random.sample(all_names, sample_size)

    def _sample_existing_insurance_plan_names(self) -> list[str]:
        all_names = list(InsurancePlan.objects.values_list("name", flat=True))
        if not all_names:
            return []
        sample_size = random.randint(1, min(5, len(all_names)))
        return random.sample(all_names, sample_size)


__all__ = [
    "ImagingCenterImportService",
    "ImagingCenterImportResult",
    "VendorImagingCenterPayload",
]


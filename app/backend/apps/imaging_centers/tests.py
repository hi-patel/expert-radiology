from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.imaging_centers.models import ImagingCenter
from apps.insurance.models import InsurancePlan
from apps.radiology.models import Modality


class ImagingCenterSearchApiTests(APITestCase):
    def setUp(self) -> None:
        mri = Modality.objects.create(name="MRI")
        ct = Modality.objects.create(name="CT")

        plan_a = InsurancePlan.objects.create(name="Plan A")
        plan_b = InsurancePlan.objects.create(name="Plan B")

        center_fast_low = ImagingCenter.objects.create(
            name="Fast Low Rating",
            address_line_1="1 Main St",
            city="City",
            state="ST",
            postal_code="00000",
            latitude=37.0,
            longitude=-122.0,
            patient_satisfaction_rating=2.5,
            review_count=10,
            referral_bonus_amount=50,
            average_turnaround_hours=8,
            patients_previously_referred=100,
            public_transit_score=80,
        )
        center_fast_low.modalities.set([mri])
        center_fast_low.insurance_plans.set([plan_a])

        center_slow_high = ImagingCenter.objects.create(
            name="Slow High Rating",
            address_line_1="2 Main St",
            city="City",
            state="ST",
            postal_code="00000",
            latitude=37.1,
            longitude=-122.1,
            patient_satisfaction_rating=4.8,
            review_count=200,
            referral_bonus_amount=None,
            average_turnaround_hours=72,
            patients_previously_referred=200,
            public_transit_score=60,
        )
        center_slow_high.modalities.set([mri, ct])
        center_slow_high.insurance_plans.set([plan_a, plan_b])

    def post(self, payload: dict) -> dict:
        url = reverse("imaging-center-search")
        response = self.client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        return response.json()

    def test_minimum_rating_filter(self) -> None:
        data = self.post(
            {
                "patient_address": "123 Main St",
                "minimum_rating": 4.0,
                "sort": ["patient_satisfaction_desc"],
            }
        )
        names = {item["name"] for item in data}
        assert "Slow High Rating" in names
        assert "Fast Low Rating" not in names

    def test_requires_all_selected_modalities(self) -> None:
        mri_id = Modality.objects.get(name="MRI").id
        ct_id = Modality.objects.get(name="CT").id

        data = self.post(
            {
                "patient_address": "123 Main St",
                "modality_ids": [mri_id, ct_id],
                "sort": [],
            }
        )
        names = {item["name"] for item in data}
        assert names == {"Slow High Rating"}

    def test_requires_any_selected_insurance(self) -> None:
        plan_b_id = InsurancePlan.objects.get(name="Plan B").id
        data = self.post(
            {
                "patient_address": "123 Main St",
                "insurance_plan_ids": [plan_b_id],
                "sort": [],
            }
        )
        names = {item["name"] for item in data}
        assert names == {"Slow High Rating"}

    def test_referral_bonus_flag(self) -> None:
        data = self.post(
            {
                "patient_address": "123 Main St",
                "requires_referral_bonus": True,
                "sort": [],
            }
        )
        names = {item["name"] for item in data}
        assert names == {"Fast Low Rating"}

from django.test import TestCase

# Create your tests here.

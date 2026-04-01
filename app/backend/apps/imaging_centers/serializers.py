from rest_framework import serializers

from apps.imaging_centers.models import ImagingCenter
from apps.insurance.models import InsurancePlan
from apps.radiology.models import Modality


class ModalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Modality
        fields = ["id", "name"]


class InsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePlan
        fields = ["id", "name"]


class ImagingCenterSerializer(serializers.ModelSerializer):
    modalities = ModalitySerializer(many=True, read_only=True)
    insurance_plans = InsurancePlanSerializer(many=True, read_only=True)
    distance_from_patient_km = serializers.FloatField(read_only=True)
    distance_from_target_km = serializers.FloatField(read_only=True)

    class Meta:
        model = ImagingCenter
        fields = [
            "id",
            "name",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "latitude",
            "longitude",
            "patient_satisfaction_rating",
            "review_count",
            "modalities",
            "insurance_plans",
            "referral_bonus_amount",
            "distance_from_patient_km",
            "distance_from_target_km",
            "average_turnaround_hours",
            "patients_previously_referred",
            "public_transit_score",
        ]


from django.db import models
from apps.insurance.models import InsurancePlan
from apps.radiology.models import Modality


class ImagingCenter(models.Model):
    name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    patient_satisfaction_rating = models.DecimalField(max_digits=2, decimal_places=1)  # 0.0–5.0
    review_count = models.PositiveIntegerField(default=0)

    modalities = models.ManyToManyField(Modality, related_name="imaging_centers", blank=True)
    insurance_plans = models.ManyToManyField(InsurancePlan, related_name="imaging_centers", blank=True)

    referral_bonus_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Flat dollar amount offered as referral bonus, if any.",
    )

    average_turnaround_hours = models.PositiveIntegerField(
        help_text="Average turnaround time in hours for typical studies."
    )

    patients_previously_referred = models.PositiveIntegerField(default=0)

    public_transit_score = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Optional public transit accessibility score (future scope).",
    )

    def __str__(self) -> str:
        return self.name


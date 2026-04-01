from django.contrib import admin

from apps.imaging_centers.models import ImagingCenter


@admin.register(ImagingCenter)
class ImagingCenterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "state",
        "patient_satisfaction_rating",
        "review_count",
        "average_turnaround_hours",
        "referral_bonus_amount",
    )
    list_filter = (
        "city",
        "state",
        "modalities",
        "insurance_plans",
    )
    search_fields = (
        "name",
        "city",
        "state",
        "postal_code",
    )
    filter_horizontal = ("modalities", "insurance_plans")


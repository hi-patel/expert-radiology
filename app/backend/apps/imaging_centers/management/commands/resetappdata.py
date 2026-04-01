from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.imaging_centers.models import ImagingCenter
from apps.imaging_centers.services.import_service import ImagingCenterImportService
from apps.insurance.models import InsurancePlan
from apps.radiology.models import Modality


class Command(BaseCommand):
    help = (
        "Reset core application data for imaging centers, modalities, and insurance "
        "plans, then repopulate with mock imaging center data."
    )

    def handle(self, *args, **options) -> None:
        self.stdout.write(self.style.WARNING("Resetting application data..."))

        with transaction.atomic():
            ImagingCenter.objects.all().delete()
            Modality.objects.all().delete()
            InsurancePlan.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Cleared imaging_centers, modalities, and insurance plans."))

        # Repopulate imaging center data using the mock import service.
        service = ImagingCenterImportService(total_centers=1000)
        result = service.import_mock_data()

        self.stdout.write(
            self.style.SUCCESS(
                f"Repopulated imaging centers from mock vendor payload "
                f"(created={result.created_count}, updated={result.updated_count})."
            )
        )


from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.imaging_centers.models import ImagingCenter
from apps.imaging_centers.services.import_service import ImagingCenterImportService
from apps.insurance.models import InsurancePlan
from apps.insurance.services import InsurancePlanImportService
from apps.radiology.models import Modality
from apps.radiology.services import ModalityImportService


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

        # Repopulate core reference data first so imaging centers can attach to it.
        modality_service = ModalityImportService()
        modality_result = modality_service.import_mock_data()
        self.stdout.write(
            self.style.SUCCESS(
                f"Repopulated modalities from mock vendor payload "
                f"(created={modality_result.created_count}, updated={modality_result.updated_count})."
            )
        )

        insurance_service = InsurancePlanImportService(total_plans=10)
        insurance_result = insurance_service.import_mock_data()
        self.stdout.write(
            self.style.SUCCESS(
                f"Repopulated insurance plans from mock vendor payload "
                f"(created={insurance_result.created_count}, updated={insurance_result.updated_count})."
            )
        )

        # Finally, repopulate imaging center data using the mock import service.
        center_service = ImagingCenterImportService(total_centers=1000)
        center_result = center_service.import_mock_data()

        self.stdout.write(
            self.style.SUCCESS(
                f"Repopulated imaging centers from mock vendor payload "
                f"(created={center_result.created_count}, updated={center_result.updated_count})."
            )
        )


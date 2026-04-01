from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypedDict

from apps.insurance.models import InsurancePlan


class VendorInsurancePlanPayload(TypedDict):
    id: str
    name: str
    carrier: str
    metal_level: str | None


@dataclass
class InsurancePlanImportResult:
    created_count: int
    updated_count: int


class InsurancePlanImportService:
    """
    Import service that pretends to consume a vendor API of insurance plans and
    normalises it into our InsurancePlan table.
    """

    def __init__(self, *, total_plans: int = 10) -> None:
        self.total_plans = total_plans

    def import_mock_data(self) -> InsurancePlanImportResult:
        payload = list(self._build_mock_vendor_payload())
        return self._import_from_vendor_payload(payload)

    def _import_from_vendor_payload(
        self, payload: Iterable[VendorInsurancePlanPayload]
    ) -> InsurancePlanImportResult:
        created = 0
        updated = 0

        existing_by_name: dict[str, InsurancePlan] = {
            p.name: p for p in InsurancePlan.objects.all()
        }

        for item in payload:
            plan = existing_by_name.get(item["name"])
            if plan is None:
                InsurancePlan.objects.create(name=item["name"])
                created += 1
            else:
                # Pattern left in place for future extra fields.
                updated += 1

        return InsurancePlanImportResult(created_count=created, updated_count=updated)

    def _build_mock_vendor_payload(self) -> Iterable[VendorInsurancePlanPayload]:
        """
        Stand‑in for a vendor endpoint like GET /insurance‑plans.
        """
        carriers = [
            "BlueShield Advantage",
            "United Health Choice",
            "Aetna Radiology Network",
            "Cigna Imaging Preferred",
            "Kaiser Permanente",
            "Humana Diagnostic",
            "Anthem Plus",
            "Molina Specialty",
            "Oscar Imaging Access",
            "Community Health Partners",
        ]

        metal_levels: list[str | None] = ["Bronze", "Silver", "Gold", "Platinum", None]

        for idx, carrier in enumerate(carriers[: self.total_plans], start=1):
            plan_name = f"{carrier} Plan"
            yield VendorInsurancePlanPayload(
                id=f"plan-{idx}",
                name=plan_name,
                carrier=carrier,
                metal_level=metal_levels[(idx - 1) % len(metal_levels)],
            )


__all__ = [
    "InsurancePlanImportService",
    "InsurancePlanImportResult",
    "VendorInsurancePlanPayload",
]


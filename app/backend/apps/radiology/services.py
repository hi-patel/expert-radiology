from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, TypedDict

from apps.radiology.models import Modality


class VendorModalityPayload(TypedDict):
    id: str
    name: str
    aliases: List[str]


@dataclass
class ModalityImportResult:
    created_count: int
    updated_count: int


class ModalityImportService:
    """
    Import service that pretends to consume a vendor API describing imaging
    modalities and normalises that into our Modality table.
    """

    def __init__(self) -> None:
        ...

    def import_mock_data(self) -> ModalityImportResult:
        payload = list(self._build_mock_vendor_payload())
        return self._import_from_vendor_payload(payload)

    def _import_from_vendor_payload(
        self, payload: Iterable[VendorModalityPayload]
    ) -> ModalityImportResult:
        created = 0
        updated = 0

        existing_by_name: dict[str, Modality] = {
            m.name: m for m in Modality.objects.all()
        }

        for item in payload:
            modality = existing_by_name.get(item["name"])
            if modality is None:
                Modality.objects.create(name=item["name"])
                created += 1
            else:
                # Nothing else to update yet; keep pattern for future metadata.
                updated += 1

        return ModalityImportResult(created_count=created, updated_count=updated)

    def _build_mock_vendor_payload(self) -> Iterable[VendorModalityPayload]:
        """
        Stand‑in for a vendor endpoint like GET /modalities.
        """
        modalities: list[tuple[str, list[str]]] = [
            ("MRI", ["Magnetic Resonance Imaging"]),
            ("CT", ["Computed Tomography", "CAT Scan"]),
            ("X‑ray", ["Radiography"]),
            ("Ultrasound", ["Sonography"]),
            ("Mammography", []),
            ("PET", ["Positron Emission Tomography"]),
            ("SPECT", ["Single Photon Emission CT"]),
            ("DEXA", ["Bone Density"]),
            ("Fluoroscopy", []),
            ("Interventional Radiology", ["IR"]),
        ]

        for idx, (name, aliases) in enumerate(modalities, start=1):
            yield VendorModalityPayload(id=f"mod-{idx}", name=name, aliases=aliases)


__all__ = [
    "ModalityImportService",
    "ModalityImportResult",
    "VendorModalityPayload",
]


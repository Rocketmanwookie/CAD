# SPDX-License-Identifier: MIT
"""Approval-gated vendor CAx asset acquisition manifests.

This module never downloads vendor content. It records the official product
source and desired asset formats so a user can obtain files through the
manufacturer's permitted portal and attach a local, checksummed reference.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from controls_wb.hardware_catalog import HardwareCatalog, HardwarePart, line_catalog, part_by_name


SIEMENS_CAX_PORTAL_URL = "https://www.siemens.com/en-us/support/documentation-downloads/"


@dataclass(frozen=True)
class VendorAssetRequest:
    manufacturer: str
    product_line: str
    part_number: str
    part_name: str
    source_url: str
    requested_formats: tuple[str, ...] = ("STEP", "PDF")
    acquisition_status: str = "manual_review_required"
    portal_url: str = SIEMENS_CAX_PORTAL_URL

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["requested_formats"] = list(self.requested_formats)
        return payload


def selected_siemens_asset_requests(
    catalog: HardwareCatalog, line_name: str, cpu_name: str, module_names: tuple[str, ...] = ()
) -> list[VendorAssetRequest]:
    """Build a deterministic request list for selected Siemens planning parts."""
    line = line_catalog(catalog, "Siemens", line_name)
    if line is None:
        return []
    parts: list[HardwarePart] = []
    cpu = part_by_name(line.cpus, cpu_name)
    if cpu is not None:
        parts.append(cpu)
    for name in module_names:
        part = part_by_name(line.io_modules, name)
        if part is not None:
            parts.append(part)
    requests = []
    for part in parts:
        source = catalog.sources.get(part.source_id)
        requests.append(VendorAssetRequest(
            manufacturer="Siemens",
            product_line=line_name,
            part_number=part.part_number,
            part_name=part.name,
            source_url=source.url if source else "",
        ))
    return requests


def vendor_asset_manifest_json(requests: list[VendorAssetRequest]) -> str:
    return json.dumps([request.to_dict() for request in requests], indent=2, sort_keys=True) + "\n"

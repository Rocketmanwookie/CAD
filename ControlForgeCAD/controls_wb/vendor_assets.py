# SPDX-License-Identifier: MIT
"""Approval-gated vendor CAx asset acquisition manifests.

This module never downloads vendor content. It records the official product
source and desired asset formats so a user can obtain files through the
manufacturer's permitted portal and attach a local, checksummed reference.
"""

from __future__ import annotations

import json
import csv
from dataclasses import asdict, dataclass
from io import StringIO

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
    cad_match_status: str = "unverified"

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
        raise ValueError(f"Unknown Siemens product line: {line_name!r}")
    parts: list[HardwarePart] = []
    cpu = part_by_name(line.cpus, cpu_name)
    if cpu is None:
        raise ValueError(f"Unknown Siemens CPU selection: {cpu_name!r}")
    parts.append(cpu)
    if module_names and cpu.max_signal_modules is None:
        raise ValueError(f"Signal-module limit is unknown for {cpu.name!r}; verify the catalog limit before export")
    if cpu.max_signal_modules is not None and len(module_names) > cpu.max_signal_modules:
        raise ValueError(f"Selected {len(module_names)} signal modules exceed CPU limit {cpu.max_signal_modules}")
    for name in module_names:
        part = part_by_name(line.io_modules, name)
        if part is None:
            raise ValueError(f"Unknown Siemens I/O module selection: {name!r}")
        parts.append(part)
    requests = []
    for part in parts:
        if not part.part_number.strip():
            raise ValueError(f"Missing manufacturer part number for {part.name!r}")
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


def vendor_part_numbers_csv(requests: list[VendorAssetRequest]) -> str:
    """Return a deterministic vendor-neutral part-number/quantity import list."""
    quantities: dict[tuple[str, str], int] = {}
    for request in requests:
        manufacturer = request.manufacturer.strip()
        part_number = request.part_number.strip()
        if not manufacturer or not part_number:
            raise ValueError(f"Missing manufacturer or part number for {request.part_name!r}")
        key = (manufacturer, part_number)
        quantities[key] = quantities.get(key, 0) + 1
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=("Manufacturer", "PartNumber", "Quantity"), lineterminator="\n")
    writer.writeheader()
    for (manufacturer, part_number), quantity in sorted(quantities.items()):
        writer.writerow({"Manufacturer": manufacturer, "PartNumber": part_number, "Quantity": quantity})
    return output.getvalue()


def main(argv=None) -> int:
    """Write a selected-parts handoff to stdout, or report errors on stderr."""
    import argparse
    import sys

    from controls_wb.hardware_catalog import load_hardware_catalog

    parser = argparse.ArgumentParser(description="Export selected Siemens catalog parts for CAx handoff.")
    parser.add_argument("--line", default="S7-1200")
    parser.add_argument("--cpu", required=True, help="Exact catalog CPU name")
    parser.add_argument("--module", action="append", default=[], help="Exact module name; repeat for quantity")
    parser.add_argument("--format", choices=("csv", "part-numbers", "manifest"), default="csv")
    args = parser.parse_args(argv)
    try:
        requests = selected_siemens_asset_requests(
            load_hardware_catalog(), args.line, args.cpu, tuple(args.module)
        )
        if args.format == "manifest":
            result = vendor_asset_manifest_json(requests)
        elif args.format == "part-numbers":
            result = "".join(number + "\n" for number in sorted({r.part_number.strip() for r in requests}))
        else:
            result = vendor_part_numbers_csv(requests)
    except (ValueError, OSError) as exc:
        print(f"Parts export failed: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

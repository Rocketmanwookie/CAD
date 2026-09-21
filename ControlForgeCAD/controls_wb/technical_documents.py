# SPDX-License-Identifier: MIT
"""Datasheet links and acceptance-test plans derived from the CAD request manifest."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from xml.etree import ElementTree as ET


REGISTRY_NAMESPACE = "https://whrsdaparty.github.io/ceproject/technical-documents/0.1"
ET.register_namespace("cedoc", REGISTRY_NAMESPACE)


@dataclass(frozen=True)
class DatasheetLink:
    request_id: str
    manufacturer: str
    product_family: str
    requested_part: str
    part_key: str
    selection_state: str
    status: str
    official_lookup_url: str
    local_path: str = ""
    sha256: str = ""
    revision: str = ""
    document_date: str = ""


@dataclass(frozen=True)
class AcceptanceTest:
    request_id: str
    test_id: str
    title: str
    instruction: str
    required_evidence: str
    status: str = "Not started"


TEST_DEFINITIONS = {
    "identity": (
        "Part identity",
        "Confirm manufacturer, exact order number, family, lifecycle state, and downloaded file identity agree.",
        "Manufacturer product page or datasheet plus recorded order number",
    ),
    "datasheet": (
        "Datasheet provenance",
        "Store the official datasheet, source URL, revision or publication date, and SHA-256 checksum.",
        "Local datasheet file, source URL, and checksum",
    ),
    "geometry": (
        "CAD geometry and units",
        "Open the 3D model, verify units and overall dimensions against the official dimensional drawing, and check for corrupt or excessive geometry.",
        "Dimension comparison and rendered CAD preview",
    ),
    "mounting": (
        "Mounting and clearance",
        "Verify mounting method, insertion point, orientation, panel cutout or DIN-rail engagement, and required service/thermal clearance envelope.",
        "Mounting drawing and clearance properties",
    ),
    "pins": (
        "Terminal and port map",
        "Match every schematic pin and 3D connection port to an official terminal designation, function, electrical type, and stable catalog terminal key.",
        "Official connection diagram and terminal-map comparison",
    ),
    "iec_symbol": (
        "IEC schematic symbol",
        "Validate the IEC symbol geometry, intelligent pins, default tag family, orientation, and parent/child cross-references.",
        "Rendered IEC symbol and pin-list comparison",
    ),
    "nfpa_symbol": (
        "NFPA/JIC schematic symbol",
        "Validate the NFPA/JIC symbol geometry, intelligent pins, default tag family, orientation, and parent/child cross-references.",
        "Rendered NFPA/JIC symbol and pin-list comparison",
    ),
    "ratings": (
        "Electrical ratings",
        "Verify voltage, current, power, frequency, utilization category, interrupting/SCCR data, and environmental ratings applicable to the selected part.",
        "Datasheet rating table and normalized equipment properties",
    ),
    "cables": (
        "Cables workbench integration",
        "Create or connect the physical route through the FreeCAD Cables workbench and confirm route length and endpoints return to the canonical CE wire or cable record.",
        "Cables route object link, endpoint identities, and calculated length",
    ),
    "safety": (
        "Safety evidence",
        "Verify safety approvals and intended architecture attributes against the risk assessment; do not infer PL, SIL, category, or diagnostic coverage from geometry.",
        "Certificate/manual reference and safety-review record",
    ),
    "io_mapping": (
        "Software and I/O mapping",
        "Confirm channel or device labels, addresses, data type, scaling, and terminal identities map consistently to the I/O and wiring schedules.",
        "I/O schedule row and matching terminal/channel records",
    ),
    "termination": (
        "Termination treatment",
        "Verify conductor range, strip length, ferrule or listed lug, crimp tool/profile, and terminal compatibility; reject bare stranded-wire terminations.",
        "Terminal instructions and termination inspection record",
    ),
}


def load_cad_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "RequestID", "System", "Category", "ManufacturerPreference", "ProductFamily",
        "RequestedPart", "MLFBOrSearchKey", "PartSelection", "SourceURL",
        "ThreeDModel", "IECSymbol", "NFPAJICSymbol", "TerminalPinMap",
        "CableWorkbenchAsset",
    }
    if not rows:
        raise ValueError("CAD request manifest is empty.")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"CAD request manifest is missing columns: {', '.join(sorted(missing))}")
    ids = [row["RequestID"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("CAD request manifest contains duplicate RequestID values.")
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def datasheet_links(
    rows: list[dict[str, str]],
    local_datasheets: dict[str, Path] | None = None,
) -> tuple[DatasheetLink, ...]:
    local_datasheets = local_datasheets or {}
    links = []
    for row in rows:
        part_key = row["MLFBOrSearchKey"].strip()
        local_path = local_datasheets.get(part_key)
        if local_path is not None and local_path.is_file():
            status = "linked_local"
            path_text = str(local_path.resolve())
            checksum = sha256_file(local_path)
        elif row["PartSelection"] == "Exact catalog seed":
            status = "pending_download"
            path_text = ""
            checksum = ""
        else:
            status = "pending_part_selection"
            path_text = ""
            checksum = ""
        links.append(
            DatasheetLink(
                request_id=row["RequestID"],
                manufacturer=row["ManufacturerPreference"],
                product_family=row["ProductFamily"],
                requested_part=row["RequestedPart"],
                part_key=part_key,
                selection_state=row["PartSelection"],
                status=status,
                official_lookup_url=row["SourceURL"].strip(),
                local_path=path_text,
                sha256=checksum,
            )
        )
    return tuple(links)


def acceptance_tests(rows: list[dict[str, str]]) -> tuple[AcceptanceTest, ...]:
    tests = []
    for row in rows:
        test_ids = ["identity", "datasheet"]
        if row["ThreeDModel"] == "Required":
            test_ids.extend(("geometry", "mounting"))
        if row["TerminalPinMap"] == "Required":
            test_ids.append("pins")
        if row["IECSymbol"] == "Required":
            test_ids.append("iec_symbol")
        if row["NFPAJICSymbol"] == "Required":
            test_ids.append("nfpa_symbol")
        category_text = f"{row['System']} {row['Category']} {row['RequestedPart']}".lower()
        if any(token in category_text for token in ("power", "protection", "contactor", "overload", "outlet", "instrument", "terminal", "plc", "hmi", "operator")):
            test_ids.append("ratings")
        if row["CableWorkbenchAsset"] == "Required":
            test_ids.append("cables")
        if any(token in category_text for token in ("safety", "emergency", "pull-rope", "guard", "fail-safe")):
            test_ids.append("safety")
        if any(token in category_text for token in ("plc", "i/o", "hmi", "instrument", "sensor", "stack light")):
            test_ids.append("io_mapping")
        if row["TerminalPinMap"] == "Required" or row["CableWorkbenchAsset"] == "Required":
            test_ids.append("termination")
        for test_id in dict.fromkeys(test_ids):
            title, instruction, evidence = TEST_DEFINITIONS[test_id]
            tests.append(AcceptanceTest(row["RequestID"], test_id, title, instruction, evidence))
    return tuple(tests)


def datasheet_csv(links: tuple[DatasheetLink, ...]) -> str:
    output = StringIO()
    fields = tuple(DatasheetLink.__dataclass_fields__)
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for link in links:
        writer.writerow({field: getattr(link, field) for field in fields})
    return output.getvalue()


def acceptance_test_csv(tests: tuple[AcceptanceTest, ...]) -> str:
    output = StringIO()
    fields = tuple(AcceptanceTest.__dataclass_fields__)
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for test in tests:
        writer.writerow({field: getattr(test, field) for field in fields})
    return output.getvalue()


def registry_xml(links: tuple[DatasheetLink, ...], tests: tuple[AcceptanceTest, ...]) -> str:
    root = ET.Element(
        f"{{{REGISTRY_NAMESPACE}}}TechnicalDocumentRegistry",
        {"schemaVersion": "0.1.0", "recordCount": str(len(links))},
    )
    definitions = ET.SubElement(root, f"{{{REGISTRY_NAMESPACE}}}TestDefinitions")
    for test_id, (title, instruction, evidence) in TEST_DEFINITIONS.items():
        ET.SubElement(
            definitions,
            f"{{{REGISTRY_NAMESPACE}}}TestDefinition",
            {"id": test_id, "title": title, "instruction": instruction, "requiredEvidence": evidence},
        )
    tests_by_request: dict[str, list[AcceptanceTest]] = {}
    for test in tests:
        tests_by_request.setdefault(test.request_id, []).append(test)
    records = ET.SubElement(root, f"{{{REGISTRY_NAMESPACE}}}EquipmentDocumentLinks")
    for link in links:
        record = ET.SubElement(
            records,
            f"{{{REGISTRY_NAMESPACE}}}EquipmentDocumentLink",
            {
                "requestId": link.request_id,
                "manufacturer": link.manufacturer,
                "productFamily": link.product_family,
                "requestedPart": link.requested_part,
                "partKey": link.part_key,
                "selectionState": link.selection_state,
            },
        )
        attributes = {"type": "datasheet", "status": link.status}
        for key, value in (
            ("officialLookupUrl", link.official_lookup_url), ("localPath", link.local_path),
            ("sha256", link.sha256), ("revision", link.revision), ("documentDate", link.document_date),
        ):
            if value:
                attributes[key] = value
        ET.SubElement(record, f"{{{REGISTRY_NAMESPACE}}}Document", attributes)
        required_tests = ET.SubElement(record, f"{{{REGISTRY_NAMESPACE}}}RequiredTests")
        for test in tests_by_request.get(link.request_id, []):
            ET.SubElement(
                required_tests,
                f"{{{REGISTRY_NAMESPACE}}}RequiredTest",
                {"definitionId": test.test_id, "status": "not_started"},
            )
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True) + "\n"

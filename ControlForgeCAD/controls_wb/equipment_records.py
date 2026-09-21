# SPDX-License-Identifier: MIT
"""Read-only access to normalized equipment record XML catalogs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class EquipmentRecord:
    record_id: str
    category: str
    product_name: str
    part_number: str
    summary: str
    source_id: str
    source_locator: str
    verified: bool
    properties: dict[str, str]


@dataclass(frozen=True)
class EquipmentRecordCatalog:
    catalog_id: str
    manufacturer: str
    family: str
    edition: str
    records: tuple[EquipmentRecord, ...]


def default_siemens_records_path() -> Path:
    """Return the bundled Siemens S7-1200 record catalog path."""
    return Path(__file__).resolve().parent / "resources" / "hardware" / "siemens_s7_1200_2017.xml"


def load_equipment_records(path: Path | None = None) -> EquipmentRecordCatalog:
    """Load one normalized equipment record catalog."""
    catalog_path = path if path is not None else default_siemens_records_path()
    root = ET.parse(catalog_path).getroot()
    if root.tag != "equipmentRecords":
        raise ValueError(f"Expected equipmentRecords root, got {root.tag!r}")
    records = tuple(
        EquipmentRecord(
            record_id=element.get("id", ""),
            category=element.get("category", ""),
            product_name=element.get("productName", ""),
            part_number=element.get("partNumber", ""),
            summary=(element.findtext("summary") or "").strip(),
            source_id=element.get("sourceId", ""),
            source_locator=element.get("sourceLocator", ""),
            verified=element.get("verified", "false").lower() == "true",
            properties={
                item.get("name", ""): (item.text or "").strip()
                for item in element.findall("./properties/property")
                if item.get("name")
            },
        )
        for element in root.findall("./records/record")
    )
    expected_count = int(root.get("recordCount", "0"))
    if expected_count != len(records):
        raise ValueError(f"Catalog declares {expected_count} records but contains {len(records)}")
    return EquipmentRecordCatalog(
        catalog_id=root.get("catalogId", ""),
        manufacturer=root.get("manufacturer", ""),
        family=root.get("family", ""),
        edition=root.get("edition", ""),
        records=records,
    )


def categories(catalog: EquipmentRecordCatalog) -> tuple[str, ...]:
    """Return catalog categories in alphabetical order."""
    return tuple(sorted({record.category for record in catalog.records}))


def record_by_part_number(catalog: EquipmentRecordCatalog, part_number: str) -> EquipmentRecord | None:
    """Return the exact case-insensitive part-number match."""
    target = part_number.casefold().strip()
    for record in catalog.records:
        if record.part_number.casefold() == target:
            return record
    return None


def search_records(catalog: EquipmentRecordCatalog, query: str) -> tuple[EquipmentRecord, ...]:
    """Search product names, part numbers, categories, summaries, and property values."""
    target = query.casefold().strip()
    if not target:
        return catalog.records
    matches = []
    for record in catalog.records:
        haystack = " ".join(
            (
                record.product_name,
                record.part_number,
                record.category,
                record.summary,
                *record.properties.values(),
            )
        ).casefold()
        if target in haystack:
            matches.append(record)
    return tuple(matches)

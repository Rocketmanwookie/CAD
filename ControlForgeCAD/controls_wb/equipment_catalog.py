# SPDX-License-Identifier: MIT
"""Neutral equipment taxonomy and linked-catalog loader."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class EquipmentSource:
    source_id: str
    title: str
    source_type: str
    local_path: str = ""
    url: str = ""
    revision: str = ""
    retrieved_on: str = ""


@dataclass(frozen=True)
class EquipmentField:
    name: str
    value_type: str
    required: bool = False


@dataclass(frozen=True)
class EquipmentAsset:
    kind: str
    format: str = ""
    review_required: bool = True


@dataclass(frozen=True)
class EquipmentClass:
    class_id: str
    name: str
    category: str
    implementation_phase: str
    record_status: str
    source_id: str
    source_locator: str
    description: str
    capabilities: tuple[str, ...] = ()
    required_data: tuple[EquipmentField, ...] = ()
    assets: tuple[EquipmentAsset, ...] = ()


@dataclass(frozen=True)
class LinkedCatalog:
    catalog_id: str
    kind: str
    path: str
    schema_path: str = ""


@dataclass(frozen=True)
class EquipmentCatalog:
    catalog_id: str
    schema_version: str
    sources: dict[str, EquipmentSource]
    equipment_classes: tuple[EquipmentClass, ...]
    linked_catalogs: tuple[LinkedCatalog, ...]


def default_equipment_catalog_path() -> Path:
    """Return the bundled neutral equipment catalog path."""
    return Path(__file__).resolve().parent / "resources" / "hardware" / "equipment_catalog.xml"


def load_equipment_catalog(path: Path | None = None) -> EquipmentCatalog:
    """Load the neutral equipment taxonomy and linked catalog declarations."""
    catalog_path = path if path is not None else default_equipment_catalog_path()
    root = ET.parse(catalog_path).getroot()
    if root.tag != "equipmentCatalog":
        raise ValueError(f"Expected equipmentCatalog root, got {root.tag!r}")

    sources = {
        element.get("id", ""): EquipmentSource(
            source_id=element.get("id", ""),
            title=element.get("title", ""),
            source_type=element.get("sourceType", ""),
            local_path=element.get("localPath", ""),
            url=element.get("url", ""),
            revision=element.get("revision", ""),
            retrieved_on=element.get("retrievedOn", ""),
        )
        for element in root.findall("./sources/source")
        if element.get("id")
    }
    equipment_classes = tuple(_equipment_class(element) for element in root.findall("./equipmentClasses/equipmentClass"))
    linked_catalogs = tuple(
        LinkedCatalog(
            catalog_id=element.get("id", ""),
            kind=element.get("kind", ""),
            path=element.get("path", ""),
            schema_path=element.get("schemaPath", ""),
        )
        for element in root.findall("./linkedCatalogs/catalog")
    )
    catalog = EquipmentCatalog(
        catalog_id=root.get("catalogId", ""),
        schema_version=root.get("schemaVersion", ""),
        sources=sources,
        equipment_classes=equipment_classes,
        linked_catalogs=linked_catalogs,
    )
    _validate_catalog(catalog)
    return catalog


def equipment_class_by_id(catalog: EquipmentCatalog, class_id: str) -> EquipmentClass | None:
    """Return an equipment class by its stable ID."""
    for equipment_class in catalog.equipment_classes:
        if equipment_class.class_id == class_id:
            return equipment_class
    return None


def linked_catalog_path(catalog_path: Path, linked_catalog: LinkedCatalog) -> Path:
    """Resolve a linked catalog relative to the neutral catalog file."""
    return (catalog_path.parent / linked_catalog.path).resolve()


def linked_schema_path(catalog_path: Path, linked_catalog: LinkedCatalog) -> Path | None:
    """Resolve a linked schema path when one is declared."""
    if not linked_catalog.schema_path:
        return None
    return (catalog_path.parent / linked_catalog.schema_path).resolve()


def _equipment_class(element: ET.Element) -> EquipmentClass:
    return EquipmentClass(
        class_id=element.get("id", ""),
        name=element.get("name", ""),
        category=element.get("category", ""),
        implementation_phase=element.get("implementationPhase", ""),
        record_status=element.get("recordStatus", ""),
        source_id=element.get("sourceId", ""),
        source_locator=element.get("sourceLocator", ""),
        description=(element.findtext("description") or "").strip(),
        capabilities=tuple(
            capability.text.strip()
            for capability in element.findall("./capabilities/capability")
            if capability.text and capability.text.strip()
        ),
        required_data=tuple(
            EquipmentField(
                name=field.get("name", ""),
                value_type=field.get("valueType", ""),
                required=field.get("required", "false").lower() == "true",
            )
            for field in element.findall("./requiredData/field")
        ),
        assets=tuple(
            EquipmentAsset(
                kind=asset.get("kind", ""),
                format=asset.get("format", ""),
                review_required=asset.get("reviewRequired", "true").lower() == "true",
            )
            for asset in element.findall("./assets/asset")
        ),
    )


def _validate_catalog(catalog: EquipmentCatalog) -> None:
    class_ids = [equipment_class.class_id for equipment_class in catalog.equipment_classes]
    if len(class_ids) != len(set(class_ids)):
        raise ValueError("Equipment class IDs must be unique")
    missing_sources = sorted(
        {
            equipment_class.source_id
            for equipment_class in catalog.equipment_classes
            if equipment_class.source_id not in catalog.sources
        }
    )
    if missing_sources:
        raise ValueError(f"Unknown equipment source IDs: {', '.join(missing_sources)}")

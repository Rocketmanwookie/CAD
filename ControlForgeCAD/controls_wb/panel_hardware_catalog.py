# SPDX-License-Identifier: MIT
"""Panel hardware catalog loading for starter layout placeholders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class PanelHardwarePart:
    layout_name: str
    manufacturer: str
    part_number: str
    description: str
    verified: bool = False
    source_id: str = ""


@dataclass(frozen=True)
class PanelHardwareCatalog:
    parts: tuple[PanelHardwarePart, ...]


def default_panel_catalog_path() -> Path:
    return Path(__file__).resolve().parent / "resources" / "hardware" / "panel_catalog.xml"


def load_panel_hardware_catalog(path: Path | None = None) -> PanelHardwareCatalog:
    catalog_path = path if path is not None else default_panel_catalog_path()
    root = ET.parse(catalog_path).getroot()
    return PanelHardwareCatalog(
        tuple(
            PanelHardwarePart(
                layout_name=part.get("layoutName", ""),
                manufacturer=part.get("manufacturer", ""),
                part_number=part.get("partNumber", ""),
                description=part.get("description", ""),
                verified=part.get("verified", "false").lower() == "true",
                source_id=part.get("sourceId", ""),
            )
            for part in root.findall("./parts/part")
        )
    )


def part_for_layout(catalog: PanelHardwareCatalog, layout_name: str) -> PanelHardwarePart | None:
    for part in catalog.parts:
        if part.layout_name == layout_name:
            return part
    return None

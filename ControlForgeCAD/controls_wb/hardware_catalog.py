# SPDX-License-Identifier: MIT
"""PLC hardware catalog loading and I/O expansion planning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class HardwareSource:
    title: str
    url: str = ""
    local_path: str = ""
    sha256: str = ""
    document_number: str = ""


@dataclass(frozen=True)
class HardwareCadRef:
    format: str
    local_path: str
    sha256: str = ""


@dataclass(frozen=True)
class HardwarePart:
    name: str
    part_number: str = ""
    di: int = 0
    do: int = 0
    ai: int = 0
    ao: int = 0
    verified: bool = False
    source_id: str = ""
    cad_refs: tuple[HardwareCadRef, ...] = ()


@dataclass(frozen=True)
class PlcLineCatalog:
    make: str
    line: str
    cpus: tuple[HardwarePart, ...]
    io_modules: tuple[HardwarePart, ...]
    ethernet: tuple[HardwarePart, ...]
    power: tuple[HardwarePart, ...]


@dataclass(frozen=True)
class HardwareCatalog:
    lines: tuple[PlcLineCatalog, ...]
    sources: dict[str, HardwareSource]


def default_catalog_path() -> Path:
    return Path(__file__).resolve().parent / "resources" / "hardware" / "plc_catalog.xml"


def load_hardware_catalog(path: Path | None = None) -> HardwareCatalog:
    catalog_path = path if path is not None else default_catalog_path()
    root = ET.parse(catalog_path).getroot()

    sources = {
        source.get("id", ""): HardwareSource(
            title=source.get("title", ""),
            url=source.get("url", ""),
            local_path=source.get("localPath", ""),
            sha256=source.get("sha256", ""),
            document_number=source.get("documentNumber", ""),
        )
        for source in root.findall("./sources/source")
        if source.get("id")
    }

    lines = []
    for make_element in root.findall("./make"):
        make_name = make_element.get("name", "")
        for line_element in make_element.findall("./line"):
            line_name = line_element.get("name", "")
            lines.append(
                PlcLineCatalog(
                    make=make_name,
                    line=line_name,
                    cpus=_parts(line_element, "cpus", "cpu"),
                    io_modules=_parts(line_element, "ioModules", "module"),
                    ethernet=_parts(line_element, "ethernetAdapters", "adapter"),
                    power=_parts(line_element, "powerSupplies", "powerSupply"),
                )
            )
    return HardwareCatalog(tuple(lines), sources)


def _parts(line_element: ET.Element, group_name: str, item_name: str) -> tuple[HardwarePart, ...]:
    group = line_element.find(group_name)
    if group is None:
        return ()
    return tuple(_part(item) for item in group.findall(item_name))


def _part(item: ET.Element) -> HardwarePart:
    return HardwarePart(
        name=item.get("name", ""),
        part_number=item.get("partNumber", ""),
        di=_int_attr(item, "di"),
        do=_int_attr(item, "do"),
        ai=_int_attr(item, "ai"),
        ao=_int_attr(item, "ao"),
        verified=item.get("verified", "false").lower() == "true",
        source_id=item.get("sourceId", ""),
        cad_refs=tuple(
            HardwareCadRef(
                format=cad_ref.get("format", ""),
                local_path=cad_ref.get("localPath", ""),
                sha256=cad_ref.get("sha256", ""),
            )
            for cad_ref in item.findall("./cadRefs/cadRef")
        ),
    )


def _int_attr(item: ET.Element, name: str) -> int:
    try:
        return max(int(item.get(name, "0")), 0)
    except ValueError:
        return 0


def makes(catalog: HardwareCatalog) -> tuple[str, ...]:
    return tuple(dict.fromkeys(line.make for line in catalog.lines))


def lines_for_make(catalog: HardwareCatalog, make: str) -> tuple[str, ...]:
    return tuple(line.line for line in catalog.lines if line.make == make)


def line_catalog(catalog: HardwareCatalog, make: str, line: str) -> PlcLineCatalog | None:
    for candidate in catalog.lines:
        if candidate.make == make and candidate.line == line:
            return candidate
    return None


def part_names(parts: tuple[HardwarePart, ...]) -> tuple[str, ...]:
    return tuple(part.name for part in parts)


def part_by_name(parts: tuple[HardwarePart, ...], name: str) -> HardwarePart | None:
    for part in parts:
        if part.name == name:
            return part
    return None


def io_expansion_suggestion(
    catalog: HardwareCatalog,
    make: str,
    line: str,
    cpu_name: str,
    di_count: object,
    do_count: object,
    ai_count: object,
    ao_count: object,
) -> str:
    line_data = line_catalog(catalog, make, line)
    if line_data is None:
        return "No hardware catalog entry is available for this PLC line."
    cpu = part_by_name(line_data.cpus, cpu_name)
    if cpu is None:
        return "Select a PLC CPU to calculate onboard I/O and expansion needs."

    requested = {
        "di": _count_int(di_count),
        "do": _count_int(do_count),
        "ai": _count_int(ai_count),
        "ao": _count_int(ao_count),
    }
    suggestions = []
    for io_key, requested_count in requested.items():
        target = int(requested_count * 1.2 + 0.9999)
        available_on_cpu = int(getattr(cpu, io_key))
        extra_needed = max(target - available_on_cpu, 0)
        if extra_needed == 0:
            continue
        compatible = [module for module in line_data.io_modules if int(getattr(module, io_key)) > 0]
        if not compatible:
            suggestions.append(f"{io_key.upper()}: need {extra_needed} extra; no catalog module covers it.")
            continue
        best = min(
            compatible,
            key=lambda module: (
                _module_count_for(extra_needed, int(getattr(module, io_key))) * int(getattr(module, io_key)) - extra_needed,
                _module_count_for(extra_needed, int(getattr(module, io_key))),
            ),
        )
        module_count = _module_count_for(extra_needed, int(getattr(best, io_key)))
        verification = "vendor-verified" if best.verified else "catalog-unverified"
        suggestions.append(
            f"{io_key.upper()}: target {target}, CPU {available_on_cpu}, add {module_count} x {best.name} ({best.part_number}, {verification})"
        )
    if not suggestions:
        return "CPU I/O covers requested counts with 20% spare."
    return "; ".join(suggestions)


def _count_int(value: object) -> int:
    try:
        return max(int(str(value).strip()), 0)
    except (TypeError, ValueError):
        return 0


def _module_count_for(needed: int, capacity: int) -> int:
    if needed <= 0 or capacity <= 0:
        return 0
    return (needed + capacity - 1) // capacity

# SPDX-License-Identifier: MIT
"""Project setup import adapters for lightweight text interchange formats."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


class ProjectSetupImportError(ValueError):
    """Raised when a setup import document cannot be mapped into intake values."""


@dataclass(frozen=True)
class ProjectSetupImportResult:
    """Stable adapter output before GUI normalization applies project defaults."""

    values: dict[str, str | list[str]]
    warnings: tuple[str, ...] = ()


_YAML_LIST_ITEM = re.compile(r"^-\s*(.+)$")
_UML_FACT_LINE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_ /.-]*)\s*[:=]\s*(.*?)\s*$")


FIELD_ALIASES = {
    "project": "ProjectName",
    "project_name": "ProjectName",
    "projectname": "ProjectName",
    "name": "ProjectName",
    "customer": "Customer",
    "site": "SiteLocation",
    "site_location": "SiteLocation",
    "sitelocation": "SiteLocation",
    "location": "SiteLocation",
    "deliverables": "Deliverables",
    "power": "PowerConfiguration",
    "power_configuration": "PowerConfiguration",
    "powerconfiguration": "PowerConfiguration",
    "phase_voltage": "PowerConfiguration",
    "voltage_phase": "PowerConfiguration",
    "nominal_voltage": "NominalVoltage",
    "nominalvoltage": "NominalVoltage",
    "phase_count": "PhaseCount",
    "phasecount": "PhaseCount",
    "controlled_loads": "ControlledLoads",
    "controlledloads": "ControlledLoads",
    "loads": "ControlledLoads",
    "enclosure": "EnclosureRatings",
    "enclosure_rating": "EnclosureRatings",
    "enclosure_ratings": "EnclosureRatings",
    "enclosureratings": "EnclosureRatings",
    "plc": "PlcPlatform",
    "plc_platform": "PlcPlatform",
    "plcplatform": "PlcPlatform",
    "plc_make": "PlcMake",
    "plcmake": "PlcMake",
    "make": "PlcMake",
    "plc_line": "PlcLine",
    "plcline": "PlcLine",
    "line": "PlcLine",
    "plc_cpu": "PlcCPU",
    "plccpu": "PlcCPU",
    "cpu": "PlcCPU",
    "di": "DICount",
    "di_count": "DICount",
    "dicount": "DICount",
    "digital_inputs": "DICount",
    "do": "DOCount",
    "do_count": "DOCount",
    "docount": "DOCount",
    "digital_outputs": "DOCount",
    "ai": "AICount",
    "ai_count": "AICount",
    "aicount": "AICount",
    "analog_inputs": "AICount",
    "ao": "AOCount",
    "ao_count": "AOCount",
    "aocount": "AOCount",
    "analog_outputs": "AOCount",
    "io_accessories": "IOAccessories",
    "ioaccessories": "IOAccessories",
    "accessories": "IOAccessories",
    "ethernet_adapter": "EthernetAdapter",
    "ethernetadapter": "EthernetAdapter",
    "expansion_power_supply": "ExpansionPowerSupply",
    "expansionpowersupply": "ExpansionPowerSupply",
    "communication_protocols": "CommunicationProtocols",
    "communicationprotocols": "CommunicationProtocols",
    "protocols": "CommunicationProtocols",
    "source_type": "SourceType",
    "sourcetype": "SourceType",
    "source_title": "SourceTitle",
    "sourcetitle": "SourceTitle",
    "source_stakeholder": "SourceStakeholder",
    "sourcestakeholder": "SourceStakeholder",
    "source_reference": "SourceReference",
    "sourcereference": "SourceReference",
}

LIST_FIELDS = {
    "Deliverables",
    "ControlledLoads",
    "EnclosureRatings",
    "IOAccessories",
    "CommunicationProtocols",
}

SECTION_PREFIXES = {
    "project": {
        "name": "ProjectName",
        "customer": "Customer",
        "site": "SiteLocation",
        "site_location": "SiteLocation",
        "location": "SiteLocation",
    },
    "power": {
        "configuration": "PowerConfiguration",
        "nominal_voltage": "NominalVoltage",
        "voltage": "NominalVoltage",
        "phase_count": "PhaseCount",
        "phase": "PhaseCount",
        "controlled_loads": "ControlledLoads",
        "loads": "ControlledLoads",
    },
    "plc": {
        "make": "PlcMake",
        "line": "PlcLine",
        "cpu": "PlcCPU",
        "platform": "PlcPlatform",
        "ethernet_adapter": "EthernetAdapter",
        "expansion_power_supply": "ExpansionPowerSupply",
    },
    "io": {
        "di_count": "DICount",
        "di": "DICount",
        "do_count": "DOCount",
        "do": "DOCount",
        "ai_count": "AICount",
        "ai": "AICount",
        "ao_count": "AOCount",
        "ao": "AOCount",
        "accessories": "IOAccessories",
    },
    "source": {
        "type": "SourceType",
        "title": "SourceTitle",
        "stakeholder": "SourceStakeholder",
        "reference": "SourceReference",
    },
}


def parse_project_setup(text: str, source_format: str = "auto") -> ProjectSetupImportResult:
    """Parse a setup text document into Project Intake form-value keys.

    The adapters intentionally return the same key names used by the Project
    Intake dialog, because that lets GUI code and tests reuse the existing
    normalization path. This keeps import formats as thin translators instead
    of letting every format grow its own project model.
    """
    clean_format = source_format.strip().lower()
    if clean_format == "auto":
        clean_format = "uml" if "@startuml" in text.lower() else "yaml"
    if clean_format in {"yaml", "yml"}:
        return parse_project_setup_yaml(text)
    if clean_format in {"uml", "plantuml", "puml"}:
        return parse_project_setup_uml(text)
    raise ProjectSetupImportError(f"Unsupported project setup import format: {source_format}")


def parse_project_setup_yaml(text: str) -> ProjectSetupImportResult:
    """Parse a small dependency-free YAML subset into intake form values.

    Supported shapes are deliberately boring: `key: value`, one-level sections
    such as `project:` followed by indented keys, and list items under known
    list fields. Full YAML features like anchors, multiline scalars, quoted
    escapes, or nested object arrays are left to a future PyYAML-backed adapter
    if the project decides that dependency is worth carrying.
    """
    values: dict[str, str | list[str]] = {}
    warnings: list[str] = []
    active_key = ""
    active_section = ""

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = _strip_comment(raw_line).rstrip()
        if not line.strip() or line.strip() in {"---", "..."}:
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        list_match = _YAML_LIST_ITEM.match(stripped)
        if list_match:
            if not active_key:
                warnings.append(f"Line {line_number}: list item has no supported parent key.")
                continue
            _append_value(values, active_key, _clean_scalar(list_match.group(1)))
            continue
        if ":" not in stripped:
            warnings.append(f"Line {line_number}: ignored unsupported YAML line.")
            continue

        raw_key, raw_value = stripped.split(":", 1)
        key = raw_key.strip()
        value = _clean_scalar(raw_value)
        if not value and indent == 0:
            active_section = _canonical_key(key)
            active_key = _direct_field_key(active_section)
            continue

        mapped_key = _field_key(key, active_section if indent > 0 else "")
        if mapped_key is None:
            warnings.append(f"Line {line_number}: ignored unsupported setup key {key!r}.")
            active_key = ""
            continue
        _set_value(values, mapped_key, value)
        active_key = mapped_key
        if indent == 0:
            active_section = ""

    return _finalize_result(values, warnings)


def parse_project_setup_uml(text: str) -> ProjectSetupImportResult:
    """Parse PlantUML-style setup facts into intake form values.

    This is a UML-derived adapter, not a diagram renderer. It scans class bodies,
    notes, and plain text labels for `key: value` or `key = value` facts and
    ignores PlantUML control lines. That is enough for early project setup
    diagrams while keeping the parser deterministic and FreeCAD-independent.
    """
    values: dict[str, str | list[str]] = {}
    warnings: list[str] = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or _is_uml_control_line(stripped):
            continue
        match = _UML_FACT_LINE.match(stripped.strip("{}"))
        if match is None:
            continue
        key = match.group(1).strip()
        value = _clean_scalar(match.group(2))
        mapped_key = _field_key(key)
        if mapped_key is None:
            warnings.append(f"Line {line_number}: ignored unsupported UML setup key {key!r}.")
            continue
        _set_value(values, mapped_key, value)

    return _finalize_result(values, warnings)


def _canonical_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def _canonical_lookup(value: str) -> str | None:
    return FIELD_ALIASES.get(_canonical_key(value))


def _direct_field_key(canonical_or_field: str) -> str:
    field_key = FIELD_ALIASES.get(canonical_or_field, canonical_or_field)
    return field_key if field_key in LIST_FIELDS or field_key.endswith(("Name", "Location", "Count", "Configuration", "Platform", "Make", "Line", "CPU", "Adapter", "Supply", "Type", "Title", "Stakeholder", "Reference")) else ""


def _field_key(key: str, section: str = "") -> str | None:
    canonical = _canonical_key(key)
    section_mapping = SECTION_PREFIXES.get(_canonical_key(section), {})
    if canonical in section_mapping:
        return section_mapping[canonical]
    return FIELD_ALIASES.get(canonical)


def _set_value(values: dict[str, str | list[str]], key: str, value: str) -> None:
    if key == "ControlledLoads":
        values[key] = [
            _clean_scalar(part)
            for part in value.replace(";", "\n").splitlines()
            if _clean_scalar(part)
        ]
    elif key in LIST_FIELDS:
        values[key] = _split_list(value)
    else:
        values[key] = value


def _append_value(values: dict[str, str | list[str]], key: str, value: str) -> None:
    current = values.get(key, [])
    if not isinstance(current, list):
        current = _split_list(str(current))
    current.append(value)
    values[key] = [item for item in current if item]


def _split_list(value: str) -> list[str]:
    if not value:
        return []
    if ";" in value:
        parts: Iterable[str] = value.split(";")
    elif "|" in value:
        parts = value.split("|")
    else:
        parts = value.split(",")
    return [_clean_scalar(part) for part in parts if _clean_scalar(part)]


def _strip_comment(line: str) -> str:
    for marker in (" #", "\t#"):
        if marker in line:
            return line.split(marker, 1)[0]
    return "" if line.lstrip().startswith("#") else line


def _clean_scalar(value: object) -> str:
    text = str(value).strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1].strip()
    return text


def _is_uml_control_line(line: str) -> bool:
    lower = line.lower()
    return (
        lower.startswith("@start")
        or lower.startswith("@end")
        or lower.startswith("class ")
        or lower.startswith("object ")
        or lower.startswith("note ")
        or lower in {"}", "{"}
        or "--" in line
        or ".." in line
    )


def _finalize_result(values: dict[str, str | list[str]], warnings: list[str]) -> ProjectSetupImportResult:
    if "PowerConfiguration" not in values and (
        "NominalVoltage" in values or "PhaseCount" in values
    ):
        phase = str(values.get("PhaseCount", "")).strip().removesuffix("PH")
        voltage = str(values.get("NominalVoltage", "")).strip().removesuffix("V")
        if phase and voltage:
            values["PowerConfiguration"] = f"{phase}PH {voltage}V"
    if "SourceType" not in values and values:
        values["SourceType"] = "Uploaded file / reference"
    if "SourceTitle" not in values and values:
        values["SourceTitle"] = "Imported project setup"
    if "SourceStakeholder" not in values and values:
        values["SourceStakeholder"] = "Project manager"
    if not values:
        raise ProjectSetupImportError("No supported project setup fields were found.")
    return ProjectSetupImportResult(values=values, warnings=tuple(warnings))

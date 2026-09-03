# SPDX-License-Identifier: MIT
"""Project intake dialog helpers.

The mapping helpers in this module are pure Python. Qt imports stay inside
functions so tests and command metadata imports do not require a FreeCAD GUI.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from controls_wb.ceproject_xml import CEProjectXmlError, parse_ceproject_xml
from controls_wb.hardware_catalog import (
    line_catalog,
    lines_for_make,
    load_hardware_catalog,
    makes,
    part_names,
    io_expansion_suggestion as catalog_io_expansion_suggestion,
)
from controls_wb.intake import SourceRecordType
from controls_wb.model.project import create_or_update_project, ensure_project_properties, intake_to_project_properties
from controls_wb.power_loads import estimated_total_amps, format_load_lines, parse_load_lines
from controls_wb.setup_import import ProjectSetupImportError, parse_project_setup

HARDWARE_CATALOG = load_hardware_catalog()
PLC_LINES_BY_MAKE = {make: lines_for_make(HARDWARE_CATALOG, make) for make in makes(HARDWARE_CATALOG)}
PROJECT_SETUP_GUIDE = Path(__file__).resolve().parents[2] / "docs" / "project-setup-hardware-catalog.md"

POWER_CONFIGURATIONS = (
    "1PH 120V",
    "1PH 240V",
    "3PH 208V",
    "3PH 240V",
    "3PH 480V",
    "3PH 600V",
)

ENCLOSURE_RATING_OPTIONS = (
    "UL Listed",
    "NEMA 12",
    "NEMA 4",
    "NEMA 4X",
    "IP65",
    "Explosion proof",
)

IO_ACCESSORY_OPTIONS = (
    "Remote / modular I/O bank",
    "Ethernet I/O adapter",
    "I/O terminal bases",
    "Expansion power supply",
)

COMMUNICATION_PROTOCOL_OPTIONS = (
    "PROFINET",
    "PROFIBUS",
    "Modbus TCP",
    "Modbus RTU",
    "EtherNet/IP",
    "DeviceNet",
)

SOURCE_TYPE_LABELS = {
    "Manual entry": SourceRecordType.MANUAL_ENTRY.value,
    "Customer email": SourceRecordType.EMAIL.value,
    "Meeting note": SourceRecordType.MEETING_NOTE.value,
    "Phone call": SourceRecordType.PHONE_CALL.value,
    "Field note": SourceRecordType.FIELD_NOTE.value,
    "Vendor quote": SourceRecordType.VENDOR_QUOTE.value,
    "Uploaded file / reference": SourceRecordType.UPLOADED_FILE.value,
}

SETUP_SOURCE_ID = "SRC-PROJECT-SETUP-001"
CEPROJECT_IMPORT_SOURCE_ID_PREFIX = "SRC-CEPROJECT-IMPORT-"
SETUP_SOURCE_FIELDS = (
    ("ProjectName", "project.name"),
    ("NominalVoltage", "powerFeed.nominalVoltage"),
    ("PhaseCount", "powerFeed.phaseCount"),
    ("EnclosureRating", "environment.enclosureRating"),
    ("PlcPlatform", "controls.plcPlatform"),
    ("SensorCount", "io.sensorCount"),
)

CEPROJECT_IMPORT_REQUIRED_KEYS = ("id", "projectId", "projectName", "xmlText")


@dataclass(frozen=True)
class IntakeFormField:
    key: str
    label: str
    property_name: str


CORE_INTAKE_FORM_FIELDS = (
    IntakeFormField("ProjectName", "Project name", "ProjectName"),
    IntakeFormField("Customer", "Customer", "Customer"),
    IntakeFormField("SiteLocation", "Site/location", "SiteLocation"),
    IntakeFormField("Deliverables", "Deliverables", "Deliverables"),
)

PLC_IO_FORM_FIELDS = (
    IntakeFormField("PlcMake", "PLC make", "PlcMake"),
    IntakeFormField("PlcLine", "PLC line", "PlcLine"),
    IntakeFormField("PlcCPU", "PLC CPU", "PlcCPU"),
    IntakeFormField("DICount", "DI count", "DICount"),
    IntakeFormField("DOCount", "DO count", "DOCount"),
    IntakeFormField("AICount", "AI count", "AICount"),
    IntakeFormField("AOCount", "AO count", "AOCount"),
    IntakeFormField("IOAccessories", "I/O accessories", "IOAccessories"),
    IntakeFormField("EthernetAdapter", "Ethernet adapter", "EthernetAdapter"),
    IntakeFormField("ExpansionPowerSupply", "Expansion power supply", "ExpansionPowerSupply"),
    IntakeFormField("CommunicationProtocols", "Communication protocols", "CommunicationProtocols"),
)

POWER_LOAD_FORM_FIELDS = (
    IntakeFormField("ControlledLoads", "Controlled loads", "ControlledLoads"),
)


def parse_deliverables(value: str | list[str] | tuple[str, ...] | set[str]) -> list[str]:
    if isinstance(value, str):
        raw_items = value.split(",")
    else:
        raw_items = list(value)
    return sorted({str(item).strip() for item in raw_items if str(item).strip()})


def format_deliverables(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return ", ".join(parse_deliverables(value))
    if isinstance(value, (list, tuple, set)):
        return ", ".join(parse_deliverables(value))
    return str(value)


def parse_accessories(value: str | list[str] | tuple[str, ...] | set[str]) -> list[str]:
    return parse_deliverables(value)


def format_accessories(value: object) -> str:
    return format_deliverables(value)


def parse_multiselect(value: str | list[str] | tuple[str, ...] | set[str]) -> list[str]:
    return parse_deliverables(value)


def format_multiselect(value: object) -> str:
    return format_deliverables(value)


def parse_power_configuration(value: str) -> tuple[str, str]:
    text = str(value).strip().upper()
    if not text:
        return "", ""
    parts = text.split()
    if len(parts) != 2:
        return "", text.removesuffix("V")
    phase = parts[0].removesuffix("PH")
    voltage = parts[1].removesuffix("V")
    return voltage, phase


def power_configuration_from_values(voltage: object, phase_count: object) -> str:
    voltage_text = str(voltage or "").strip().removesuffix("V")
    phase_text = str(phase_count or "").strip().removesuffix("PH")
    candidate = f"{phase_text}PH {voltage_text}V" if voltage_text and phase_text else ""
    return candidate if candidate in POWER_CONFIGURATIONS else "3PH 480V"


def plc_lines_for_make(make: str) -> tuple[str, ...]:
    return PLC_LINES_BY_MAKE.get(make, ())


def normalized_plc_line(make: str, line: str) -> str:
    lines = plc_lines_for_make(make)
    clean_line = str(line).strip()
    if clean_line in lines:
        return clean_line
    return lines[0] if lines else clean_line


def plc_platform_from_make_line(make: str, line: str) -> str:
    clean_make = str(make).strip()
    clean_line = str(line).strip()
    return " ".join(part for part in (clean_make, clean_line) if part)


def plc_cpu_options(make: str, line: str) -> tuple[str, ...]:
    line_data = line_catalog(HARDWARE_CATALOG, make, line)
    return part_names(line_data.cpus) if line_data else ()


def hardware_dropdown_options(make: str, line: str, key: str) -> tuple[str, ...]:
    line_data = line_catalog(HARDWARE_CATALOG, make, line)
    if line_data is None:
        return ()
    if key == "ethernet":
        return part_names(line_data.ethernet)
    if key == "power":
        return part_names(line_data.power)
    return ()


def _safe_count(value: object) -> str:
    try:
        count = int(str(value).strip())
    except (TypeError, ValueError):
        return ""
    return str(max(count, 0))


def total_input_count(di_count: object, ai_count: object) -> str:
    total = int(_safe_count(di_count) or "0") + int(_safe_count(ai_count) or "0")
    return str(total) if total else ""


def io_expansion_suggestion(
    make: str,
    line: str,
    cpu: str,
    di_count: object,
    do_count: object,
    ai_count: object,
    ao_count: object,
) -> str:
    return catalog_io_expansion_suggestion(
        HARDWARE_CATALOG,
        make,
        line,
        cpu,
        di_count,
        do_count,
        ai_count,
        ao_count,
    )


def source_type_labels() -> tuple[str, ...]:
    return tuple(SOURCE_TYPE_LABELS)


def source_type_value_from_label(label: str) -> str:
    return SOURCE_TYPE_LABELS.get(label, SourceRecordType.MANUAL_ENTRY.value)


def source_type_label_from_value(value: str) -> str:
    for label, source_type in SOURCE_TYPE_LABELS.items():
        if source_type == value:
            return label
    return "Manual entry"


def _field_value(document, field_id: str) -> str:
    field = document.intake.fields.get(field_id)
    return field.value if field is not None else ""


def _plc_make_line_from_platform(platform: str) -> tuple[str, str]:
    clean_platform = str(platform).strip()
    for make, lines in PLC_LINES_BY_MAKE.items():
        for line in lines:
            if clean_platform == plc_platform_from_make_line(make, line):
                return make, line
            if clean_platform.startswith(f"{make} ") and clean_platform.removeprefix(f"{make} ").strip() == line:
                return make, line
    if clean_platform:
        for make, lines in PLC_LINES_BY_MAKE.items():
            if clean_platform.startswith(make):
                return make, lines[0] if lines else ""
    return "Siemens", normalized_plc_line("Siemens", "")


def form_values_from_ceproject_xml(xml_text: str | bytes) -> dict[str, str]:
    """Return project-intake form values from supported CEProject XML."""
    document = parse_ceproject_xml(xml_text)
    nominal_voltage = _field_value(document, "powerFeed.nominalVoltage")
    phase_count = _field_value(document, "powerFeed.phaseCount")
    enclosure_rating = _field_value(document, "environment.enclosureRating")
    plc_platform = _field_value(document, "controls.plcPlatform")
    sensor_count = _field_value(document, "io.sensorCount")
    plc_make, plc_line = _plc_make_line_from_platform(plc_platform)
    cpu_options = plc_cpu_options(plc_make, plc_line)
    ethernet_options = hardware_dropdown_options(plc_make, plc_line, "ethernet")
    power_options = hardware_dropdown_options(plc_make, plc_line, "power")

    return {
        "ProjectName": document.intake.name,
        "Customer": "",
        "SiteLocation": "",
        "Deliverables": format_deliverables(document.intake.deliverables),
        "PowerConfiguration": power_configuration_from_values(nominal_voltage, phase_count),
        "ControlledLoads": "",
        "EnclosureRatings": enclosure_rating,
        "PlcMake": plc_make,
        "PlcLine": plc_line,
        "PlcCPU": cpu_options[0] if cpu_options else "",
        "DICount": _safe_count(sensor_count),
        "DOCount": "",
        "AICount": "",
        "AOCount": "",
        "IOAccessories": "",
        "EthernetAdapter": ethernet_options[0] if ethernet_options else "",
        "ExpansionPowerSupply": power_options[0] if power_options else "",
        "CommunicationProtocols": "",
        "SourceType": "Uploaded file / reference",
        "SourceTitle": f"Imported CEProject XML: {document.intake.name}",
        "SourceStakeholder": "Project manager",
        "SourceReference": document.intake.project_id,
    }


def form_values_from_project_setup_text(text: str, source_format: str = "auto") -> dict[str, object]:
    """Return Project Intake form values from YAML-ish or UML-derived setup text."""
    result = parse_project_setup(text, source_format)
    values = dict(result.values)
    values.setdefault("SourceType", "Uploaded file / reference")
    values.setdefault("SourceTitle", f"Imported {source_format} project setup")
    values.setdefault("SourceStakeholder", "Project manager")
    values["ImportWarnings"] = list(result.warnings)
    return values


def ceproject_import_record(xml_text: str | bytes, source_path: str = "") -> str:
    """Create a durable JSON import record for a CEProject XML upload."""
    text = xml_text.decode("utf-8") if isinstance(xml_text, bytes) else str(xml_text)
    document = parse_ceproject_xml(text)
    digest = sha256(text.encode("utf-8")).hexdigest()[:12]
    return json.dumps(
        {
            "id": digest,
            "projectId": document.intake.project_id,
            "projectName": document.intake.name,
            "schemaVersion": document.intake.schema_version,
            "sourcePath": source_path,
            "xmlText": text,
        },
        sort_keys=True,
    )


def ceproject_import_records_from_project(obj: object | None) -> list[dict[str, str]]:
    records = []
    for raw_record in getattr(obj, "CEProjectImports", []) if obj is not None else []:
        try:
            record = json.loads(raw_record)
        except (TypeError, ValueError):
            continue
        if all(record.get(key) for key in CEPROJECT_IMPORT_REQUIRED_KEYS):
            records.append(record)
    return records


def merge_ceproject_import_records(existing_records: object, new_record: str | None) -> list[str]:
    records_by_id = {}
    for raw_record in list(existing_records or []):
        try:
            record = json.loads(raw_record)
        except (TypeError, ValueError):
            continue
        if all(record.get(key) for key in CEPROJECT_IMPORT_REQUIRED_KEYS):
            records_by_id[record["id"]] = json.dumps(record, sort_keys=True)
    if new_record:
        try:
            record = json.loads(new_record)
        except (TypeError, ValueError):
            record = {}
        if all(record.get(key) for key in CEPROJECT_IMPORT_REQUIRED_KEYS):
            records_by_id[record["id"]] = json.dumps(record, sort_keys=True)
    return [records_by_id[key] for key in sorted(records_by_id)]


def ceproject_import_label(record: dict[str, str]) -> str:
    name = record.get("projectName", "CEProject XML")
    project_id = record.get("projectId", "")
    source_path = record.get("sourcePath", "")
    suffix = Path(source_path).name if source_path else project_id
    return f"{name} ({suffix})" if suffix else name


def _source_records_by_id(raw_records: object) -> dict[str, str]:
    records = {}
    for raw_record in list(raw_records or []):
        try:
            record = json.loads(raw_record)
        except (TypeError, ValueError):
            continue
        record_id = record.get("id")
        if record_id:
            records[record_id] = json.dumps(record, sort_keys=True)
    return records


def _ceproject_import_source_record(record: dict[str, str]) -> str:
    import_id = record.get("id", "")
    return json.dumps(
        {
            "id": f"{CEPROJECT_IMPORT_SOURCE_ID_PREFIX}{import_id}",
            "type": SourceRecordType.UPLOADED_FILE.value,
            "title": f"Imported CEProject XML: {record.get('projectName', 'CEProject XML')}",
            "stakeholder": "Project manager",
            "fieldIds": [
                "project.name",
                "powerFeed.nominalVoltage",
                "powerFeed.phaseCount",
                "environment.enclosureRating",
                "controls.plcPlatform",
                "io.sensorCount",
            ],
            "reference": record.get("sourcePath", "") or record.get("projectId", ""),
            "receivedOn": "",
        },
        sort_keys=True,
    )


def apply_ceproject_import_to_project(obj: object, record: dict[str, str]) -> None:
    """Preserve metadata from a remembered CEProject XML import on the project object."""
    document = parse_ceproject_xml(record["xmlText"])
    imported_properties = intake_to_project_properties(document.intake)
    obj.ProjectId = imported_properties["ProjectId"]
    obj.SchemaVersion = imported_properties["SchemaVersion"]
    obj.Contacts = imported_properties["Contacts"]
    obj.IntakeQuestions = imported_properties["IntakeQuestions"]

    records_by_id = _source_records_by_id(imported_properties["SourceRecords"])
    records_by_id.update(_source_records_by_id(getattr(obj, "SourceRecords", [])))
    import_source = json.loads(_ceproject_import_source_record(record))
    records_by_id[import_source["id"]] = json.dumps(import_source, sort_keys=True)
    obj.SourceRecords = [records_by_id[key] for key in sorted(records_by_id)]


def _setup_source_field_ids(normalized: dict[str, object]) -> list[str]:
    field_ids = []
    for property_name, field_id in SETUP_SOURCE_FIELDS:
        value = normalized.get(property_name, "")
        if isinstance(value, list):
            has_value = bool(value)
        else:
            has_value = bool(str(value).strip())
        if has_value:
            field_ids.append(field_id)
    return field_ids


def setup_source_record_from_form(values: dict[str, object], normalized: dict[str, object]) -> str | None:
    field_ids = _setup_source_field_ids(normalized)
    if not field_ids:
        return None
    title = str(values.get("SourceTitle", "")).strip() or "Project setup"
    stakeholder = str(values.get("SourceStakeholder", "")).strip() or "Project manager"
    source_type = source_type_value_from_label(str(values.get("SourceType", "")))
    reference = str(values.get("SourceReference", "")).strip()
    return json.dumps(
        {
            "id": SETUP_SOURCE_ID,
            "type": source_type,
            "title": title,
            "stakeholder": stakeholder,
            "fieldIds": field_ids,
            "reference": reference,
            "receivedOn": "",
        },
        sort_keys=True,
    )


def _merge_setup_source_record(existing_records: object, setup_source_record: str | None) -> list[str]:
    records = []
    for record in list(existing_records or []):
        try:
            payload = json.loads(record)
        except (TypeError, ValueError):
            records.append(record)
            continue
        if payload.get("id") != SETUP_SOURCE_ID:
            records.append(record)
    if setup_source_record:
        records.append(setup_source_record)
    return records


def form_values_from_project(obj: object | None) -> dict[str, str]:
    values: dict[str, str] = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        value = getattr(obj, field.property_name, "") if obj is not None else ""
        values[field.key] = format_deliverables(value) if field.key == "Deliverables" else str(value or "")
    for field in PLC_IO_FORM_FIELDS:
        value = getattr(obj, field.property_name, "") if obj is not None else ""
        if field.key in {"IOAccessories", "CommunicationProtocols"}:
            values[field.key] = format_multiselect(value)
        else:
            values[field.key] = str(value or "")
    for field in POWER_LOAD_FORM_FIELDS:
        value = getattr(obj, field.property_name, "") if obj is not None else ""
        values[field.key] = format_load_lines(value)
    if not values["ProjectName"]:
        values["ProjectName"] = "Controls Project"
    if not values["Deliverables"]:
        values["Deliverables"] = "ioList, panelLayout"
    values["PowerConfiguration"] = str(getattr(obj, "PowerConfiguration", "") if obj is not None else "") or power_configuration_from_values(
        getattr(obj, "NominalVoltage", "") if obj is not None else "",
        getattr(obj, "PhaseCount", "") if obj is not None else "",
    )
    values["EnclosureRatings"] = format_multiselect(
        getattr(obj, "EnclosureRatings", "") if obj is not None else ""
    ) or str(getattr(obj, "EnclosureRating", "") if obj is not None else "")
    if not values["PlcMake"]:
        platform = str(getattr(obj, "PlcPlatform", "") if obj is not None else "")
        values["PlcMake"] = "Allen-Bradley" if "Allen" in platform or "ControlLogix" in platform or "CompactLogix" in platform else "Siemens"
    values["PlcLine"] = normalized_plc_line(values["PlcMake"], values["PlcLine"])
    cpu_options = plc_cpu_options(values["PlcMake"], values["PlcLine"])
    if values["PlcCPU"] not in cpu_options:
        values["PlcCPU"] = cpu_options[0] if cpu_options else ""
    ethernet_options = hardware_dropdown_options(values["PlcMake"], values["PlcLine"], "ethernet")
    if values["EthernetAdapter"] not in ethernet_options:
        values["EthernetAdapter"] = ethernet_options[0] if ethernet_options else ""
    power_options = hardware_dropdown_options(values["PlcMake"], values["PlcLine"], "power")
    if values["ExpansionPowerSupply"] not in power_options:
        values["ExpansionPowerSupply"] = power_options[0] if power_options else ""
    values["SourceType"] = "Manual entry"
    values["SourceTitle"] = "Project setup"
    values["SourceStakeholder"] = "Project manager"
    values["SourceReference"] = ""
    for record in getattr(obj, "SourceRecords", []) if obj is not None else []:
        try:
            payload = json.loads(record)
        except (TypeError, ValueError):
            continue
        if payload.get("id") == SETUP_SOURCE_ID:
            values["SourceType"] = source_type_label_from_value(payload.get("type", ""))
            values["SourceTitle"] = payload.get("title", "") or "Project setup"
            values["SourceStakeholder"] = payload.get("stakeholder", "") or "Project manager"
            values["SourceReference"] = payload.get("reference", "")
    return values


def normalized_form_values(values: dict[str, str]) -> dict[str, object]:
    normalized: dict[str, object] = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        value = values.get(field.key, "")
        normalized[field.property_name] = parse_deliverables(value) if field.key == "Deliverables" else str(value).strip()
    power_configuration = str(
        values.get("PowerConfiguration", "")
        or power_configuration_from_values(values.get("NominalVoltage", ""), values.get("PhaseCount", ""))
    ).strip() or "3PH 480V"
    if power_configuration not in POWER_CONFIGURATIONS:
        power_configuration = "3PH 480V"
    nominal_voltage, phase_count = parse_power_configuration(power_configuration)
    normalized["PowerConfiguration"] = power_configuration
    normalized["NominalVoltage"] = nominal_voltage
    normalized["PhaseCount"] = phase_count
    enclosure_ratings = parse_multiselect(values.get("EnclosureRatings", "") or values.get("EnclosureRating", ""))
    normalized["EnclosureRatings"] = enclosure_ratings
    normalized["EnclosureRating"] = ", ".join(enclosure_ratings)
    plc_make = str(values.get("PlcMake", "Siemens")).strip() or "Siemens"
    if plc_make not in PLC_LINES_BY_MAKE:
        plc_make = "Siemens"
    plc_line = normalized_plc_line(plc_make, values.get("PlcLine", ""))
    normalized["PlcMake"] = plc_make
    normalized["PlcLine"] = plc_line
    cpu_options = plc_cpu_options(plc_make, plc_line)
    plc_cpu = str(values.get("PlcCPU", "")).strip()
    normalized["PlcCPU"] = plc_cpu if plc_cpu in cpu_options else (cpu_options[0] if cpu_options else "")
    normalized["PlcPlatform"] = plc_platform_from_make_line(plc_make, plc_line)
    normalized["DICount"] = _safe_count(values.get("DICount", ""))
    normalized["DOCount"] = _safe_count(values.get("DOCount", ""))
    normalized["AICount"] = _safe_count(values.get("AICount", ""))
    normalized["AOCount"] = _safe_count(values.get("AOCount", ""))
    normalized["SensorCount"] = total_input_count(normalized["DICount"], normalized["AICount"])
    normalized["IOAccessories"] = parse_accessories(values.get("IOAccessories", ""))
    ethernet_options = hardware_dropdown_options(plc_make, plc_line, "ethernet")
    ethernet_adapter = str(values.get("EthernetAdapter", "")).strip()
    normalized["EthernetAdapter"] = ethernet_adapter if ethernet_adapter in ethernet_options else (ethernet_options[0] if ethernet_options else "")
    power_options = hardware_dropdown_options(plc_make, plc_line, "power")
    expansion_power = str(values.get("ExpansionPowerSupply", "")).strip()
    normalized["ExpansionPowerSupply"] = expansion_power if expansion_power in power_options else (power_options[0] if power_options else "")
    normalized["CommunicationProtocols"] = parse_multiselect(values.get("CommunicationProtocols", ""))
    normalized["ControlledLoads"] = parse_load_lines(values.get("ControlledLoads", ""))
    normalized["EstimatedLoadAmps"] = estimated_total_amps(
        normalized["ControlledLoads"],
        normalized["NominalVoltage"],
        normalized["PhaseCount"],
    )
    normalized["IOExpansionSuggestion"] = io_expansion_suggestion(
        plc_make,
        plc_line,
        str(normalized["PlcCPU"]),
        normalized["DICount"],
        normalized["DOCount"],
        normalized["AICount"],
        normalized["AOCount"],
    )
    if not normalized["ProjectName"]:
        normalized["ProjectName"] = "Controls Project"
    return normalized


def apply_form_values_to_project(obj: object, values: dict[str, str]) -> object:
    normalized = normalized_form_values(values)
    for property_name, value in normalized.items():
        setattr(obj, property_name, value)
    setup_source_record = setup_source_record_from_form(values, normalized)
    setattr(
        obj,
        "SourceRecords",
        _merge_setup_source_record(getattr(obj, "SourceRecords", []), setup_source_record),
    )
    obj.CEProjectImports = merge_ceproject_import_records(
        getattr(obj, "CEProjectImports", []),
        values.get("CEProjectImportRecord"),
    )
    selected_import_id = str(values.get("SelectedCEProjectImportId", "")).strip()
    for record in ceproject_import_records_from_project(obj):
        if record.get("id") == selected_import_id:
            apply_ceproject_import_to_project(obj, record)
            break
    return obj


def existing_project_object(document: object) -> object | None:
    for obj in getattr(document, "Objects", []) or []:
        if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables"):
            return obj
    return None


def create_or_update_project_from_form(document: object, values: dict[str, str]) -> object:
    normalized = normalized_form_values(values)
    obj = existing_project_object(document)
    if obj is not None:
        if hasattr(obj, "addProperty"):
            ensure_project_properties(obj)
    else:
        obj = create_or_update_project(document, name=str(normalized["ProjectName"]))
    for property_name, value in normalized.items():
        setattr(obj, property_name, value)
    setup_source_record = setup_source_record_from_form(values, normalized)
    obj.SourceRecords = _merge_setup_source_record(
        getattr(obj, "SourceRecords", []),
        setup_source_record,
    )
    obj.CEProjectImports = merge_ceproject_import_records(
        getattr(obj, "CEProjectImports", []),
        values.get("CEProjectImportRecord"),
    )
    selected_import_id = str(values.get("SelectedCEProjectImportId", "")).strip()
    for record in ceproject_import_records_from_project(obj):
        if record.get("id") == selected_import_id:
            apply_ceproject_import_to_project(obj, record)
            break
    return obj


def _qt_widgets():
    errors = []
    for module_name in ("PySide.QtGui", "PySide2.QtWidgets", "PySide6.QtWidgets"):
        try:
            module = __import__(module_name, fromlist=["QtWidgets"])
            if module_name == "PySide.QtGui":
                return module
            return module
        except Exception as exc:  # pragma: no cover - depends on FreeCAD Qt runtime
            errors.append(exc)
    raise RuntimeError("Qt/PySide is unavailable.") from errors[-1] if errors else None


def show_project_intake_dialog(document: object, parent=None, console=None) -> object | None:
    """Show a modal project intake dialog and create/update CE_Project on submit."""
    QtWidgets = _qt_widgets()
    existing = existing_project_object(document)
    initial_values = form_values_from_project(existing)

    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Project Intake")
    layout = QtWidgets.QVBoxLayout(dialog)
    guide_link = QtWidgets.QLabel(
        f'<a href="{PROJECT_SETUP_GUIDE.as_uri()}">Project setup hardware catalog guide</a>'
    )
    guide_link.setOpenExternalLinks(True)
    layout.addWidget(guide_link)
    form = QtWidgets.QFormLayout()
    editors = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        editor = QtWidgets.QLineEdit(initial_values[field.key])
        editors[field.key] = editor
        form.addRow(field.label, editor)

    power_editor = QtWidgets.QComboBox()
    power_editor.addItems(list(POWER_CONFIGURATIONS))
    power_editor.setCurrentText(initial_values["PowerConfiguration"])
    editors["PowerConfiguration"] = power_editor
    form.addRow("Power", power_editor)

    loads_editor = QtWidgets.QTextEdit()
    loads_editor.setPlainText(initial_values["ControlledLoads"])
    loads_editor.setPlaceholderText("motor, Conveyor motor, 1, 1.5hp")
    editors["ControlledLoads"] = loads_editor
    form.addRow("Controlled loads", loads_editor)

    enclosure_editors = {}
    enclosure_box = QtWidgets.QWidget()
    enclosure_layout = QtWidgets.QVBoxLayout(enclosure_box)
    selected_enclosures = set(parse_multiselect(initial_values["EnclosureRatings"]))
    for enclosure in ENCLOSURE_RATING_OPTIONS:
        checkbox = QtWidgets.QCheckBox(enclosure)
        checkbox.setChecked(enclosure in selected_enclosures)
        enclosure_editors[enclosure] = checkbox
        enclosure_layout.addWidget(checkbox)
    layout.addLayout(form)
    layout.addWidget(enclosure_box)

    make_editor = QtWidgets.QComboBox()
    make_editor.addItems(list(PLC_LINES_BY_MAKE.keys()))
    make_editor.setCurrentText(initial_values["PlcMake"])
    line_editor = QtWidgets.QComboBox()
    cpu_editor = QtWidgets.QComboBox()
    ethernet_editor = QtWidgets.QComboBox()
    power_supply_editor = QtWidgets.QComboBox()

    def refresh_hardware():
        cpu_current = cpu_editor.currentText() or initial_values["PlcCPU"]
        ethernet_current = ethernet_editor.currentText() or initial_values["EthernetAdapter"]
        power_current = power_supply_editor.currentText() or initial_values["ExpansionPowerSupply"]
        cpu_editor.clear()
        cpu_editor.addItems(list(plc_cpu_options(make_editor.currentText(), line_editor.currentText())))
        cpu_editor.setCurrentText(cpu_current if cpu_current in plc_cpu_options(make_editor.currentText(), line_editor.currentText()) else (cpu_editor.itemText(0) if cpu_editor.count() else ""))
        ethernet_editor.clear()
        ethernet_editor.addItems(list(hardware_dropdown_options(make_editor.currentText(), line_editor.currentText(), "ethernet")))
        ethernet_editor.setCurrentText(ethernet_current if ethernet_current in hardware_dropdown_options(make_editor.currentText(), line_editor.currentText(), "ethernet") else (ethernet_editor.itemText(0) if ethernet_editor.count() else ""))
        power_supply_editor.clear()
        power_supply_editor.addItems(list(hardware_dropdown_options(make_editor.currentText(), line_editor.currentText(), "power")))
        power_supply_editor.setCurrentText(power_current if power_current in hardware_dropdown_options(make_editor.currentText(), line_editor.currentText(), "power") else (power_supply_editor.itemText(0) if power_supply_editor.count() else ""))

    def refresh_lines():
        current_line = line_editor.currentText() or initial_values["PlcLine"]
        line_editor.clear()
        line_editor.addItems(list(plc_lines_for_make(make_editor.currentText())))
        line_editor.setCurrentText(normalized_plc_line(make_editor.currentText(), current_line))
        refresh_hardware()

    make_editor.currentTextChanged.connect(lambda _text: refresh_lines())
    line_editor.currentTextChanged.connect(lambda _text: refresh_hardware())
    refresh_lines()
    editors["PlcMake"] = make_editor
    editors["PlcLine"] = line_editor
    editors["PlcCPU"] = cpu_editor
    editors["EthernetAdapter"] = ethernet_editor
    editors["ExpansionPowerSupply"] = power_supply_editor
    form.addRow("PLC make", make_editor)
    form.addRow("PLC line", line_editor)
    form.addRow("PLC CPU", cpu_editor)
    form.addRow("Ethernet adapter", ethernet_editor)
    form.addRow("Expansion power supply", power_supply_editor)

    for field in PLC_IO_FORM_FIELDS:
        if field.key in {
            "PlcMake",
            "PlcLine",
            "PlcCPU",
            "IOAccessories",
            "EthernetAdapter",
            "ExpansionPowerSupply",
            "CommunicationProtocols",
        }:
            continue
        editor = QtWidgets.QLineEdit(initial_values[field.key])
        editors[field.key] = editor
        form.addRow(field.label, editor)

    accessory_editors = {}
    accessory_box = QtWidgets.QWidget()
    accessory_layout = QtWidgets.QVBoxLayout(accessory_box)
    selected_accessories = set(parse_accessories(initial_values["IOAccessories"]))
    for accessory in IO_ACCESSORY_OPTIONS:
        checkbox = QtWidgets.QCheckBox(accessory)
        checkbox.setChecked(accessory in selected_accessories)
        accessory_editors[accessory] = checkbox
        accessory_layout.addWidget(checkbox)
    layout.addWidget(accessory_box)

    protocol_editors = {}
    protocol_box = QtWidgets.QWidget()
    protocol_layout = QtWidgets.QVBoxLayout(protocol_box)
    selected_protocols = set(parse_multiselect(initial_values["CommunicationProtocols"]))
    for protocol in COMMUNICATION_PROTOCOL_OPTIONS:
        checkbox = QtWidgets.QCheckBox(protocol)
        checkbox.setChecked(protocol in selected_protocols)
        protocol_editors[protocol] = checkbox
        protocol_layout.addWidget(checkbox)
    layout.addWidget(protocol_box)

    source_type_editor = QtWidgets.QComboBox()
    source_type_editor.addItems(list(source_type_labels()))
    source_type_editor.setCurrentText(initial_values["SourceType"])
    source_title_editor = QtWidgets.QLineEdit(initial_values["SourceTitle"])
    source_stakeholder_editor = QtWidgets.QLineEdit(initial_values["SourceStakeholder"])
    source_reference_editor = QtWidgets.QLineEdit(initial_values["SourceReference"])
    editors["SourceType"] = source_type_editor
    editors["SourceTitle"] = source_title_editor
    editors["SourceStakeholder"] = source_stakeholder_editor
    editors["SourceReference"] = source_reference_editor
    source_form = QtWidgets.QFormLayout()
    source_form.addRow("Source type", source_type_editor)
    source_form.addRow("Source title", source_title_editor)
    source_form.addRow("Source stakeholder", source_stakeholder_editor)
    source_form.addRow("Source reference", source_reference_editor)
    layout.addLayout(source_form)

    import_records = ceproject_import_records_from_project(existing)
    selected_import_id = ""
    pending_import_record = ""
    import_editor = QtWidgets.QComboBox()

    def refresh_import_editor(current_id: str = ""):
        import_editor.clear()
        for record in import_records:
            import_editor.addItem(ceproject_import_label(record))
        if current_id:
            for index, record in enumerate(import_records):
                if record.get("id") == current_id:
                    import_editor.setCurrentIndex(index)
                    break

    def apply_imported_form_values(imported_values: dict[str, object]):
        for key in ("ProjectName", "Customer", "SiteLocation", "Deliverables"):
            editor = editors.get(key)
            if editor is not None and hasattr(editor, "setText"):
                editor.setText(format_deliverables(imported_values.get(key, "")) if key == "Deliverables" else str(imported_values.get(key, "")))

        loads_editor.setPlainText(format_load_lines(imported_values.get("ControlledLoads", "")))
        power_editor.setCurrentText(str(imported_values.get("PowerConfiguration", "")))
        make_editor.setCurrentText(str(imported_values.get("PlcMake", "")))
        line_editor.setCurrentText(str(imported_values.get("PlcLine", "")))
        cpu_editor.setCurrentText(str(imported_values.get("PlcCPU", "")))
        ethernet_editor.setCurrentText(str(imported_values.get("EthernetAdapter", "")))
        power_supply_editor.setCurrentText(str(imported_values.get("ExpansionPowerSupply", "")))

        for key in ("DICount", "DOCount", "AICount", "AOCount"):
            editor = editors.get(key)
            if editor is not None and hasattr(editor, "setText"):
                editor.setText(str(imported_values.get(key, "")))

        selected_enclosure_values = set(parse_multiselect(imported_values.get("EnclosureRatings", "")))
        for enclosure, checkbox in enclosure_editors.items():
            checkbox.setChecked(enclosure in selected_enclosure_values)

        selected_accessory_values = set(parse_accessories(imported_values.get("IOAccessories", "")))
        for accessory, checkbox in accessory_editors.items():
            checkbox.setChecked(accessory in selected_accessory_values)

        selected_protocol_values = set(parse_multiselect(imported_values.get("CommunicationProtocols", "")))
        for protocol, checkbox in protocol_editors.items():
            checkbox.setChecked(protocol in selected_protocol_values)

        source_type_editor.setCurrentText(str(imported_values.get("SourceType", "Uploaded file / reference")))
        source_title_editor.setText(str(imported_values.get("SourceTitle", "Imported project setup")))
        source_stakeholder_editor.setText(str(imported_values.get("SourceStakeholder", "Project manager")))
        source_reference_editor.setText(str(imported_values.get("SourceReference", "")))

    def apply_import_values(record: dict[str, str]):
        apply_imported_form_values(form_values_from_ceproject_xml(record["xmlText"]))

    def selected_import_record():
        index = import_editor.currentIndex()
        if 0 <= index < len(import_records):
            return import_records[index]
        return None

    def apply_selected_import():
        nonlocal selected_import_id
        record = selected_import_record()
        if record is None:
            return
        try:
            apply_import_values(record)
        except CEProjectXmlError as exc:
            QtWidgets.QMessageBox.critical(dialog, "CEProject XML Import", str(exc))
            return
        selected_import_id = record["id"]

    def import_ceproject_xml():
        nonlocal pending_import_record, selected_import_id
        result = QtWidgets.QFileDialog.getOpenFileName(
            dialog,
            "Import CEProject XML",
            str(Path.home()),
            "CEProject XML (*.ceproject.xml *.xml);;XML files (*.xml);;All files (*)",
        )
        source_path = result[0] if isinstance(result, tuple) else result
        if not source_path:
            return
        try:
            xml_text = Path(source_path).read_text(encoding="utf-8")
            pending_import_record = ceproject_import_record(xml_text, source_path)
            record = json.loads(pending_import_record)
            import_records[:] = [candidate for candidate in import_records if candidate.get("id") != record["id"]]
            import_records.append(record)
            import_records.sort(key=lambda candidate: ceproject_import_label(candidate))
            refresh_import_editor(record["id"])
            apply_import_values(record)
            selected_import_id = record["id"]
        except (OSError, UnicodeError, CEProjectXmlError) as exc:
            QtWidgets.QMessageBox.critical(dialog, "CEProject XML Import", str(exc))

    def import_project_setup_text():
        result = QtWidgets.QFileDialog.getOpenFileName(
            dialog,
            "Import Project Setup",
            str(Path.home()),
            "Project setup (*.yaml *.yml *.puml *.plantuml *.uml *.txt);;All files (*)",
        )
        source_path = result[0] if isinstance(result, tuple) else result
        if not source_path:
            return
        suffix = Path(source_path).suffix.lower()
        source_format = "plantuml" if suffix in {".puml", ".plantuml", ".uml"} else "yaml"
        try:
            setup_text = Path(source_path).read_text(encoding="utf-8")
            imported_values = form_values_from_project_setup_text(setup_text, source_format)
            imported_values["SourceReference"] = source_path
            apply_imported_form_values(imported_values)
            warnings = imported_values.get("ImportWarnings", [])
            if console is not None and warnings:
                for warning in warnings:
                    console.PrintWarning(f"Project setup import: {warning}\n")
        except (OSError, UnicodeError, ProjectSetupImportError) as exc:
            QtWidgets.QMessageBox.critical(dialog, "Project Setup Import", str(exc))

    import_box = QtWidgets.QWidget()
    import_layout = QtWidgets.QHBoxLayout(import_box)
    import_button = QtWidgets.QPushButton("Import CEProject XML")
    import_setup_button = QtWidgets.QPushButton("Import Setup YAML/UML")
    apply_import_button = QtWidgets.QPushButton("Apply selected XML")
    import_button.clicked.connect(import_ceproject_xml)
    import_setup_button.clicked.connect(import_project_setup_text)
    apply_import_button.clicked.connect(apply_selected_import)
    import_layout.addWidget(import_editor)
    import_layout.addWidget(import_button)
    import_layout.addWidget(import_setup_button)
    import_layout.addWidget(apply_import_button)
    refresh_import_editor()
    form.addRow("Saved CEProject XML", import_box)

    buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
    )
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    exec_dialog = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if exec_dialog() != QtWidgets.QDialog.Accepted:
        return None

    values = {}
    for key, editor in editors.items():
        if hasattr(editor, "currentText"):
            values[key] = editor.currentText()
        elif hasattr(editor, "toPlainText"):
            values[key] = editor.toPlainText()
        else:
            values[key] = editor.text()
    values["IOAccessories"] = [
        accessory
        for accessory, checkbox in accessory_editors.items()
        if checkbox.isChecked()
    ]
    values["EnclosureRatings"] = [
        enclosure
        for enclosure, checkbox in enclosure_editors.items()
        if checkbox.isChecked()
    ]
    values["CommunicationProtocols"] = [
        protocol
        for protocol, checkbox in protocol_editors.items()
        if checkbox.isChecked()
    ]
    values["CEProjectImportRecord"] = pending_import_record
    values["SelectedCEProjectImportId"] = selected_import_id
    project = create_or_update_project_from_form(document, values)
    if console is not None:
        console.PrintMessage(f"Controls project intake updated: {project.ProjectName}\n")
        console.PrintMessage(f"I/O expansion plan: {project.IOExpansionSuggestion}\n")
    if getattr(project, "IOExpansionSuggestion", ""):
        QtWidgets.QMessageBox.information(
            dialog,
            "I/O Expansion Plan",
            project.IOExpansionSuggestion,
        )
    return project

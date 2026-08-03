# SPDX-License-Identifier: MIT
"""Starter I/O list model and CSV export helpers."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from io import StringIO
from typing import Any

from controls_wb.missing_data import project_object_to_intake


IO_LIST_HEADERS = (
    "Tag",
    "Address",
    "Description",
    "SignalType",
    "Device",
    "Rack",
    "Slot",
    "Channel",
    "Terminal",
    "SourceRecordIds",
    "MappingStatus",
)


@dataclass(frozen=True)
class IOSignalType:
    key: str
    label: str
    signal_type: str
    tag_prefix: str
    address_kind: str


IO_SIGNAL_TYPES = (
    IOSignalType("digital_input", "Digital Input", "digital_input", "DI", "input_bit"),
    IOSignalType("digital_output", "Digital Output", "digital_output", "DO", "output_bit"),
    IOSignalType("analog_input", "Analog Input", "analog_input", "AI", "input_word"),
    IOSignalType("analog_output", "Analog Output", "analog_output", "AO", "output_word"),
    IOSignalType("relay", "Relay", "relay", "RLY", "relay"),
)

COUNT_PROPERTY_BY_SIGNAL_TYPE = {
    "digital_input": "DICount",
    "digital_output": "DOCount",
    "analog_input": "AICount",
    "analog_output": "AOCount",
}

STARTER_DESCRIPTION_BY_SIGNAL_TYPE = {
    "digital_input": "Starter digital input",
    "digital_output": "Starter digital output",
    "analog_input": "Starter analog input",
    "analog_output": "Starter analog output",
}


@dataclass(frozen=True)
class IOSignal:
    tag: str
    description: str
    signal_type: str
    address: str = ""
    device: str = ""
    rack: str = ""
    slot: str = ""
    channel: str = ""
    terminal: str = ""
    source_record_ids: tuple[str, ...] = ()
    mapping_status: str = "unmapped"

    def to_csv_row(self) -> dict[str, Any]:
        return {
            "Tag": self.tag,
            "Address": self.address,
            "Description": self.description,
            "SignalType": self.signal_type,
            "Device": self.device,
            "Rack": self.rack,
            "Slot": self.slot,
            "Channel": self.channel,
            "Terminal": self.terminal,
            "SourceRecordIds": ";".join(self.source_record_ids),
            "MappingStatus": self.mapping_status,
        }

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_record_ids"] = list(self.source_record_ids)
        return payload


def io_signal_type_for_key(key: str) -> IOSignalType:
    for signal_type in IO_SIGNAL_TYPES:
        if signal_type.key == key:
            return signal_type
    raise ValueError(f"Unsupported I/O signal type: {key}")


def io_signal_type_labels() -> tuple[str, ...]:
    return tuple(signal_type.label for signal_type in IO_SIGNAL_TYPES)


def io_signal_type_key_from_label(label: str) -> str:
    for signal_type in IO_SIGNAL_TYPES:
        if signal_type.label == label:
            return signal_type.key
    raise ValueError(f"Unsupported I/O signal type label: {label}")


def _tag_index(tag: str, prefix: str) -> int:
    marker = f"{prefix}-"
    if not tag.startswith(marker):
        return 0
    try:
        return int(tag.removeprefix(marker))
    except ValueError:
        return 0


def next_signal_index(signals: list[IOSignal], signal_type: IOSignalType) -> int:
    return max((_tag_index(signal.tag, signal_type.tag_prefix) for signal in signals), default=0) + 1


def auto_address(signal_type: IOSignalType, index: int) -> str:
    zero_based = max(index - 1, 0)
    if signal_type.address_kind == "input_bit":
        return f"%I{zero_based // 8}.{zero_based % 8}"
    if signal_type.address_kind == "output_bit":
        return f"%Q{zero_based // 8}.{zero_based % 8}"
    if signal_type.address_kind == "input_word":
        return f"%IW{zero_based * 2}"
    if signal_type.address_kind == "output_word":
        return f"%QW{zero_based * 2}"
    if signal_type.address_kind == "relay":
        return f"RLY-{index:04d}"
    return ""


def create_labeled_io_signal(signal_type_key: str, label: str, existing_signals: list[IOSignal] | None = None) -> IOSignal:
    signal_type = io_signal_type_for_key(signal_type_key)
    existing = existing_signals or []
    index = next_signal_index(existing, signal_type)
    clean_label = str(label).strip() or signal_type.label
    return IOSignal(
        tag=f"{signal_type.tag_prefix}-{index:04d}",
        address=auto_address(signal_type, index),
        description=clean_label,
        signal_type=signal_type.signal_type,
        device=clean_label,
        mapping_status="mapped" if signal_type.address_kind == "relay" else "addressed",
    )


def serialize_io_signal(signal: IOSignal) -> str:
    return json.dumps(signal.to_dict(), sort_keys=True)


def deserialize_io_signal(record: str | dict[str, Any]) -> IOSignal:
    payload = json.loads(record) if isinstance(record, str) else dict(record)
    source_record_ids = payload.get("source_record_ids", payload.get("sourceRecordIds", ()))
    return IOSignal(
        tag=str(payload.get("tag", "")),
        address=str(payload.get("address", "")),
        description=str(payload.get("description", "")),
        signal_type=str(payload.get("signal_type", payload.get("signalType", ""))),
        device=str(payload.get("device", "")),
        rack=str(payload.get("rack", "")),
        slot=str(payload.get("slot", "")),
        channel=str(payload.get("channel", "")),
        terminal=str(payload.get("terminal", "")),
        source_record_ids=tuple(str(source_id) for source_id in source_record_ids),
        mapping_status=str(payload.get("mapping_status", payload.get("mappingStatus", "unmapped"))),
    )


def explicit_io_signals_from_project(project: object) -> list[IOSignal]:
    signals: list[IOSignal] = []
    for record in getattr(project, "IOSignals", []) or []:
        try:
            signal = deserialize_io_signal(record)
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
        if signal.tag:
            signals.append(signal)
    return signals


def append_io_signal_to_project(project: object, signal_type_key: str, label: str) -> IOSignal:
    existing = explicit_io_signals_from_project(project)
    signal = create_labeled_io_signal(signal_type_key, label, existing)
    records = list(getattr(project, "IOSignals", []) or [])
    records.append(serialize_io_signal(signal))
    setattr(project, "IOSignals", records)
    return signal


def _safe_sensor_count(value: str) -> int:
    try:
        count = int(str(value).strip())
    except (TypeError, ValueError):
        return 0
    return max(count, 0)


def _typed_count(project: object, signal_type_key: str) -> int:
    property_name = COUNT_PROPERTY_BY_SIGNAL_TYPE[signal_type_key]
    return _safe_sensor_count(getattr(project, property_name, ""))


def _has_typed_counts(project: object) -> bool:
    return any(
        str(getattr(project, property_name, "")).strip()
        for property_name in COUNT_PROPERTY_BY_SIGNAL_TYPE.values()
    )


def _starter_signals_for_type(
    signal_type_key: str,
    count: int,
    existing_signals: list[IOSignal],
    source_record_ids: tuple[str, ...] = (),
) -> list[IOSignal]:
    signal_type = io_signal_type_for_key(signal_type_key)
    existing_count = sum(
        1 for signal in existing_signals
        if signal.signal_type == signal_type.signal_type
    )
    remaining_count = max(count - existing_count, 0)
    start_index = next_signal_index(existing_signals, signal_type)
    return [
        IOSignal(
            tag=f"{signal_type.tag_prefix}-{index:04d}",
            address=auto_address(signal_type, index),
            description=f"{STARTER_DESCRIPTION_BY_SIGNAL_TYPE[signal_type_key]} {index}",
            signal_type=signal_type.signal_type,
            device=f"{signal_type.label} {index}",
            source_record_ids=source_record_ids,
            mapping_status="addressed",
        )
        for index in range(start_index, start_index + remaining_count)
    ]


def starter_io_signals_from_project(project: object, existing_signals: list[IOSignal] | None = None) -> list[IOSignal]:
    """Build starter I/O signals from the current project intake data."""
    intake = project_object_to_intake(project)
    existing = existing_signals or []
    source_record_ids = tuple(
        sorted(
            source.source_id
            for source in intake.source_records.values()
            if "io.sensorCount" in source.field_ids
        )
    )

    if _has_typed_counts(project):
        signals: list[IOSignal] = []
        for signal_type_key in COUNT_PROPERTY_BY_SIGNAL_TYPE:
            signals.extend(
                _starter_signals_for_type(
                    signal_type_key,
                    _typed_count(project, signal_type_key),
                    existing + signals,
                    source_record_ids if signal_type_key in {"digital_input", "analog_input"} else (),
                )
            )
        return signals

    sensor_field = intake.fields.get("io.sensorCount")
    count = _safe_sensor_count(sensor_field.value if sensor_field else "")
    if count == 0 and not existing:
        return [
            IOSignal(
                tag="IO-UNASSIGNED-001",
                description="Sensor count is missing or not numeric",
                signal_type="unknown",
                source_record_ids=source_record_ids,
                mapping_status="missing",
            )
        ]

    return _starter_signals_for_type(
        "digital_input",
        count,
        existing,
        source_record_ids,
    )


def io_signals_from_objects(objects: list[object]) -> list[IOSignal]:
    signals: list[IOSignal] = []
    for obj in objects:
        if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables"):
            explicit_signals = explicit_io_signals_from_project(obj)
            signals.extend(explicit_signals)
            signals.extend(starter_io_signals_from_project(obj, explicit_signals))
    return signals


def io_list_csv(signals: list[IOSignal]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=list(IO_LIST_HEADERS), lineterminator="\n")
    writer.writeheader()
    for signal in signals:
        writer.writerow(signal.to_csv_row())
    return output.getvalue()


def unmapped_io_findings(signals: list[IOSignal]) -> list[str]:
    findings = []
    for signal in signals:
        if signal.mapping_status == "missing":
            findings.append(f"ERROR: {signal.tag} has no usable I/O source data.")
        elif signal.mapping_status == "unmapped":
            findings.append(f"WARNING: {signal.tag} is not mapped to PLC rack/slot/channel.")
    return findings


def io_mapping_summary(signals: list[IOSignal]) -> str | None:
    missing_count = sum(1 for signal in signals if signal.mapping_status == "missing")
    unmapped_count = sum(
        1 for signal in signals
        if signal.mapping_status == "unmapped"
    )
    missing_label = "signal" if missing_count == 1 else "signals"
    unmapped_label = "signal" if unmapped_count == 1 else "signals"

    if missing_count and unmapped_count:
        return (
            f"WARNING: I/O list has {missing_count} {missing_label} with missing source data "
            f"and {unmapped_count} {unmapped_label} not mapped to PLC rack/slot/channel. "
            "See integracab_io_list.csv for details."
        )
    if missing_count:
        return (
            f"ERROR: I/O list has {missing_count} {missing_label} with missing source data. "
            "See integracab_io_list.csv for details."
        )
    if unmapped_count:
        return (
            f"WARNING: I/O list has {unmapped_count} {unmapped_label} not mapped to "
            "PLC rack/slot/channel. See integracab_io_list.csv for details."
        )
    return None

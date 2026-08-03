# SPDX-License-Identifier: MIT
"""Starter I/O list model and CSV export helpers."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from io import StringIO
from typing import Any

from controls_wb.missing_data import project_object_to_intake


IO_LIST_HEADERS = (
    "Tag",
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
class IOSignal:
    tag: str
    description: str
    signal_type: str
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


def _safe_sensor_count(value: str) -> int:
    try:
        count = int(str(value).strip())
    except (TypeError, ValueError):
        return 0
    return max(count, 0)


def starter_io_signals_from_project(project: object) -> list[IOSignal]:
    """Build starter I/O signals from the current project intake data."""
    intake = project_object_to_intake(project)
    sensor_field = intake.fields.get("io.sensorCount")
    count = _safe_sensor_count(sensor_field.value if sensor_field else "")
    source_record_ids = tuple(
        sorted(
            source.source_id
            for source in intake.source_records.values()
            if "io.sensorCount" in source.field_ids
        )
    )

    if count == 0:
        return [
            IOSignal(
                tag="IO-UNASSIGNED-001",
                description="Sensor count is missing or not numeric",
                signal_type="unknown",
                source_record_ids=source_record_ids,
                mapping_status="missing",
            )
        ]

    return [
        IOSignal(
            tag=f"DI-{index:04d}",
            description=f"Starter discrete input {index}",
            signal_type="digital_input",
            device=f"Sensor {index}",
            source_record_ids=source_record_ids,
            mapping_status="unmapped",
        )
        for index in range(1, count + 1)
    ]


def io_signals_from_objects(objects: list[object]) -> list[IOSignal]:
    signals: list[IOSignal] = []
    for obj in objects:
        if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables"):
            signals.extend(starter_io_signals_from_project(obj))
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
        elif signal.mapping_status != "mapped":
            findings.append(f"WARNING: {signal.tag} is not mapped to PLC rack/slot/channel.")
    return findings


def io_mapping_summary(signals: list[IOSignal]) -> str | None:
    missing_count = sum(1 for signal in signals if signal.mapping_status == "missing")
    unmapped_count = sum(
        1 for signal in signals
        if signal.mapping_status not in {"mapped", "missing"}
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

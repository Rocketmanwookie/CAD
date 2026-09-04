# SPDX-License-Identifier: MIT
"""Traceable signal-to-terminal-to-wire connection records."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from io import StringIO


CONNECTION_SCHEDULE_HEADERS = (
    "ConnectionId",
    "SignalTag",
    "FieldDevice",
    "TerminalStrip",
    "Terminal",
    "WireTag",
    "PLCRack",
    "PLCSlot",
    "PLCChannel",
    "Status",
)


@dataclass(frozen=True)
class SignalConnection:
    """One cabinet-side signal path; not an electrical-schematic netlist."""

    connection_id: str
    signal_tag: str
    field_device: str = ""
    terminal_strip: str = ""
    terminal: str = ""
    wire_tag: str = ""
    plc_rack: str = ""
    plc_slot: str = ""
    plc_channel: str = ""
    status: str = "planned"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def to_csv_row(self) -> dict[str, str]:
        return {
            "ConnectionId": self.connection_id,
            "SignalTag": self.signal_tag,
            "FieldDevice": self.field_device,
            "TerminalStrip": self.terminal_strip,
            "Terminal": self.terminal,
            "WireTag": self.wire_tag,
            "PLCRack": self.plc_rack,
            "PLCSlot": self.plc_slot,
            "PLCChannel": self.plc_channel,
            "Status": self.status,
        }


def serialize_connection(connection: SignalConnection) -> str:
    return json.dumps(connection.to_dict(), sort_keys=True)


def deserialize_connection(record: str | dict[str, object]) -> SignalConnection:
    payload = json.loads(record) if isinstance(record, str) else dict(record)
    return SignalConnection(
        connection_id=str(payload.get("connection_id", payload.get("connectionId", ""))),
        signal_tag=str(payload.get("signal_tag", payload.get("signalTag", ""))),
        field_device=str(payload.get("field_device", payload.get("fieldDevice", ""))),
        terminal_strip=str(payload.get("terminal_strip", payload.get("terminalStrip", ""))),
        terminal=str(payload.get("terminal", "")),
        wire_tag=str(payload.get("wire_tag", payload.get("wireTag", ""))),
        plc_rack=str(payload.get("plc_rack", payload.get("plcRack", ""))),
        plc_slot=str(payload.get("plc_slot", payload.get("plcSlot", ""))),
        plc_channel=str(payload.get("plc_channel", payload.get("plcChannel", ""))),
        status=str(payload.get("status", "planned")),
    )


def connections_from_project(project: object) -> list[SignalConnection]:
    connections = []
    for record in getattr(project, "ConnectionRecords", []) or []:
        try:
            connection = deserialize_connection(record)
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
        if connection.connection_id and connection.signal_tag:
            connections.append(connection)
    return connections


def next_connection_id(connections: list[SignalConnection]) -> str:
    indexes = []
    for connection in connections:
        if connection.connection_id.startswith("CONN-"):
            try:
                indexes.append(int(connection.connection_id.removeprefix("CONN-")))
            except ValueError:
                pass
    return f"CONN-{max(indexes, default=0) + 1:04d}"


def append_connection_to_project(project: object, values: dict[str, object]) -> SignalConnection:
    """Persist one normalized connection record on an editable CE_Project."""
    existing = connections_from_project(project)
    connection = SignalConnection(
        connection_id=str(values.get("connection_id", "")).strip() or next_connection_id(existing),
        signal_tag=str(values.get("signal_tag", "")).strip(),
        field_device=str(values.get("field_device", "")).strip(),
        terminal_strip=str(values.get("terminal_strip", "")).strip(),
        terminal=str(values.get("terminal", "")).strip(),
        wire_tag=str(values.get("wire_tag", "")).strip(),
        plc_rack=str(values.get("plc_rack", "")).strip(),
        plc_slot=str(values.get("plc_slot", "")).strip(),
        plc_channel=str(values.get("plc_channel", "")).strip(),
        status=str(values.get("status", "planned")).strip() or "planned",
    )
    if not connection.signal_tag:
        raise ValueError("A signal tag is required for a connection record.")
    records = list(getattr(project, "ConnectionRecords", []) or [])
    records.append(serialize_connection(connection))
    setattr(project, "ConnectionRecords", records)
    return connection


def connection_schedule_csv(connections: list[SignalConnection]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=CONNECTION_SCHEDULE_HEADERS, lineterminator="\n")
    writer.writeheader()
    for connection in sorted(connections, key=lambda item: (item.signal_tag, item.connection_id)):
        writer.writerow(connection.to_csv_row())
    return output.getvalue()


def connection_findings(connections: list[SignalConnection]) -> list[str]:
    """Return deterministic data-quality findings without asserting electrical compliance."""
    findings = []
    terminal_owners: dict[tuple[str, str], str] = {}
    for connection in connections:
        for field_name, value in (
            ("field device", connection.field_device),
            ("terminal strip", connection.terminal_strip),
            ("terminal", connection.terminal),
            ("wire tag", connection.wire_tag),
        ):
            if not value:
                findings.append(f"WARNING: {connection.connection_id} is missing {field_name}.")
        if connection.terminal_strip and connection.terminal:
            key = (connection.terminal_strip, connection.terminal)
            previous = terminal_owners.get(key)
            if previous and previous != connection.connection_id:
                findings.append(
                    f"ERROR: {connection.connection_id} and {previous} use {connection.terminal_strip}:{connection.terminal}."
                )
            terminal_owners[key] = connection.connection_id
    return findings

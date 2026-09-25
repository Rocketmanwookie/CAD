# SPDX-License-Identifier: MIT
"""Traceable signal-to-terminal-to-wire connection records."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from io import StringIO

from controls_wb.identity import CERoles


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
    "PathIdentity",
    "SignalIdentity",
    "PLCDeviceIdentity",
    "TerminalStripIdentity",
    "FieldDeviceIdentity",
    "TerminalIdentities",
    "WireIdentities",
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
    path_identity: str = ""
    signal_identity: str = ""
    plc_device_identity: str = ""
    terminal_strip_identity: str = ""
    field_device_identity: str = ""
    terminal_identities: tuple[str, ...] = ()
    wire_identities: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
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
            "PathIdentity": self.path_identity,
            "SignalIdentity": self.signal_identity,
            "PLCDeviceIdentity": self.plc_device_identity,
            "TerminalStripIdentity": self.terminal_strip_identity,
            "FieldDeviceIdentity": self.field_device_identity,
            "TerminalIdentities": ";".join(self.terminal_identities),
            "WireIdentities": ";".join(self.wire_identities),
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
        path_identity=str(payload.get("path_identity", payload.get("pathIdentity", ""))),
        signal_identity=str(payload.get("signal_identity", payload.get("signalIdentity", ""))),
        plc_device_identity=str(
            payload.get("plc_device_identity", payload.get("plcDeviceIdentity", ""))
        ),
        terminal_strip_identity=str(
            payload.get("terminal_strip_identity", payload.get("terminalStripIdentity", ""))
        ),
        field_device_identity=str(
            payload.get("field_device_identity", payload.get("fieldDeviceIdentity", ""))
        ),
        terminal_identities=_identity_tuple(
            payload.get("terminal_identities", payload.get("terminalIdentities", ()))
        ),
        wire_identities=_identity_tuple(
            payload.get("wire_identities", payload.get("wireIdentities", ()))
        ),
    )


def _identity_tuple(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        values = value.split(";") if value else ()
    elif isinstance(value, (list, tuple)):
        values = value
    else:
        values = ()
    return tuple(str(item).strip() for item in values if str(item).strip())


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
        path_identity=str(values.get("path_identity", "")).strip(),
        signal_identity=str(values.get("signal_identity", "")).strip(),
        plc_device_identity=str(values.get("plc_device_identity", "")).strip(),
        terminal_strip_identity=str(values.get("terminal_strip_identity", "")).strip(),
        field_device_identity=str(values.get("field_device_identity", "")).strip(),
        terminal_identities=_identity_tuple(values.get("terminal_identities", ())),
        wire_identities=_identity_tuple(values.get("wire_identities", ())),
    )
    if not connection.signal_tag:
        raise ValueError("A signal tag is required for a connection record.")
    records = list(getattr(project, "ConnectionRecords", []) or [])
    records.append(serialize_connection(connection))
    setattr(project, "ConnectionRecords", records)
    return connection


def append_connection_for_path(project: object, path_object: object) -> SignalConnection:
    """Persist one identity-linked legacy record for a materialized typed path."""

    terminals = tuple(getattr(path_object, "TerminalObjects", []) or [])
    wires = tuple(getattr(path_object, "WireObjects", []) or [])
    if not terminals or not wires:
        raise ValueError("A typed path requires terminal and wire objects before linking a record.")
    devices = {
        str(getattr(device, "CEIdentity", "") or ""): device
        for device in (getattr(project, "ElectricalDevices", []) or [])
    }
    owner_ids = [str(getattr(terminal, "OwnerIdentity", "") or "") for terminal in terminals]
    plc_identity = owner_ids[0]
    field_identity = owner_ids[-1]
    cabinet_terminals = [
        terminal
        for terminal in terminals
        if getattr(terminal, "CERole", "") == CERoles.CABINET_TERMINAL
    ]
    strip_identity = str(
        getattr(cabinet_terminals[0], "OwnerIdentity", "") if cabinet_terminals else ""
    )

    def device_tag(identity: str) -> str:
        device = devices.get(identity)
        return str(getattr(device, "Tag", getattr(device, "Label", "")) or "")

    return append_connection_to_project(
        project,
        {
            "signal_tag": str(getattr(path_object, "SignalTag", "") or ""),
            "field_device": device_tag(field_identity),
            "terminal_strip": device_tag(strip_identity),
            "terminal": ";".join(
                str(getattr(terminal, "Designation", "") or "")
                for terminal in cabinet_terminals
            ),
            "wire_tag": ";".join(str(getattr(wire, "WireTag", "") or "") for wire in wires),
            "plc_rack": device_tag(plc_identity),
            "plc_channel": str(getattr(terminals[0], "Designation", "") or ""),
            "path_identity": str(getattr(path_object, "CEIdentity", "") or ""),
            "signal_identity": str(getattr(path_object, "SignalIdentity", "") or ""),
            "plc_device_identity": plc_identity,
            "terminal_strip_identity": strip_identity,
            "field_device_identity": field_identity,
            "terminal_identities": tuple(
                str(getattr(terminal, "CEIdentity", "") or "") for terminal in terminals
            ),
            "wire_identities": tuple(
                str(getattr(wire, "CEIdentity", "") or "") for wire in wires
            ),
        },
    )


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


def connection_reference_findings(
    connections: list[SignalConnection], objects: list[object] | tuple[object, ...]
) -> list[str]:
    """Validate optional typed-object references retained by connection records."""

    findings = []
    identity_index = {
        str(getattr(obj, "CEIdentity", "") or ""): obj
        for obj in objects
        if getattr(obj, "CEIdentity", "")
    }
    for connection in connections:
        if not connection.path_identity:
            findings.append(
                f"WARNING: {connection.connection_id} is not linked to a typed electrical path."
            )
            continue
        references = (
            ("path", connection.path_identity, {CERoles.CONNECTION_PATH}),
            ("signal", connection.signal_identity, {CERoles.SIGNAL}),
            ("PLC device", connection.plc_device_identity, {CERoles.PLC_CONTROLLER}),
            ("terminal strip", connection.terminal_strip_identity, {CERoles.TERMINAL_STRIP}),
            ("field device", connection.field_device_identity, {CERoles.FIELD_DEVICE}),
        )
        referenced_objects = {}
        for label, identity, expected_roles in references:
            if not identity:
                findings.append(
                    f"ERROR: {connection.connection_id} is missing its {label} identity reference."
                )
                continue
            referenced_objects[label] = _validate_reference(
                findings, connection.connection_id, label, identity, expected_roles, identity_index
            )
        terminal_objects = _validate_reference_sequence(
            findings,
            connection.connection_id,
            "terminal",
            connection.terminal_identities,
            {CERoles.PLC_CHANNEL_TERMINAL, CERoles.CABINET_TERMINAL, CERoles.DEVICE_TERMINAL},
            identity_index,
        )
        wire_objects = _validate_reference_sequence(
            findings,
            connection.connection_id,
            "wire",
            connection.wire_identities,
            {CERoles.WIRE},
            identity_index,
        )
        path_object = referenced_objects.get("path")
        if path_object is not None:
            _validate_path_membership(
                findings,
                connection,
                path_object,
                terminal_objects,
                wire_objects,
            )
    return findings


def _validate_reference(
    findings: list[str],
    connection_id: str,
    label: str,
    identity: str,
    expected_roles: set[str],
    identity_index: dict[str, object],
):
    obj = identity_index.get(identity)
    if obj is None:
        findings.append(f"ERROR: {connection_id} has a dangling {label} identity {identity}.")
        return None
    role = str(getattr(obj, "CERole", "") or "")
    if role not in expected_roles:
        findings.append(
            f"ERROR: {connection_id} references {label} identity {identity} with role {role or '<none>'}."
        )
        return None
    return obj


def _validate_reference_sequence(
    findings: list[str],
    connection_id: str,
    label: str,
    identities: tuple[str, ...],
    expected_roles: set[str],
    identity_index: dict[str, object],
) -> tuple[object, ...]:
    if not identities:
        findings.append(f"ERROR: {connection_id} has no {label} identity references.")
        return ()
    objects = []
    for identity in identities:
        obj = _validate_reference(
            findings, connection_id, label, identity, expected_roles, identity_index
        )
        if obj is not None:
            objects.append(obj)
    return tuple(objects)


def _validate_path_membership(
    findings: list[str],
    connection: SignalConnection,
    path_object: object,
    terminal_objects: tuple[object, ...],
    wire_objects: tuple[object, ...],
) -> None:
    path_signal_identity = str(getattr(path_object, "SignalIdentity", "") or "")
    if path_signal_identity != connection.signal_identity:
        findings.append(
            f"ERROR: {connection.connection_id} signal identity does not match its typed path."
        )
    path_terminal_ids = tuple(
        str(getattr(obj, "CEIdentity", "") or "")
        for obj in (getattr(path_object, "TerminalObjects", []) or [])
    )
    path_wire_ids = tuple(
        str(getattr(obj, "CEIdentity", "") or "")
        for obj in (getattr(path_object, "WireObjects", []) or [])
    )
    resolved_terminal_ids = tuple(str(getattr(obj, "CEIdentity", "") or "") for obj in terminal_objects)
    resolved_wire_ids = tuple(str(getattr(obj, "CEIdentity", "") or "") for obj in wire_objects)
    if resolved_terminal_ids and path_terminal_ids != connection.terminal_identities:
        findings.append(
            f"ERROR: {connection.connection_id} terminal identities do not match its typed path order."
        )
    if resolved_wire_ids and path_wire_ids != connection.wire_identities:
        findings.append(
            f"ERROR: {connection.connection_id} wire identities do not match its typed path order."
        )

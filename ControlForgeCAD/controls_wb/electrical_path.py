# SPDX-License-Identifier: MIT
"""Continuous identity-safe terminal/wire paths and derived schedules."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass

from controls_wb.identity import CERoles, is_ce_identity, validate_ce_role


PATH_FORMAT = "ceproject.connection-path/1.0"
TERMINAL_ROLES = frozenset(
    {
        CERoles.PLC_CHANNEL_TERMINAL,
        CERoles.CABINET_TERMINAL,
        CERoles.DEVICE_TERMINAL,
    }
)


@dataclass(frozen=True)
class RoutePoint:
    """One physical wire route point in millimetres."""

    x_mm: float
    y_mm: float
    z_mm: float


@dataclass(frozen=True)
class TerminalEndpoint:
    identity: str
    role: str
    owner_identity: str
    designation: str
    label: str = ""

    def validate(self) -> None:
        if not is_ce_identity(self.identity):
            raise ValueError(f"Invalid terminal identity: {self.identity}")
        if not is_ce_identity(self.owner_identity):
            raise ValueError(f"Invalid terminal owner identity: {self.owner_identity}")
        if validate_ce_role(self.role) not in TERMINAL_ROLES:
            raise ValueError(f"Role is not a terminal role: {self.role}")
        if not self.designation.strip():
            raise ValueError(f"Terminal {self.identity} requires a designation.")


@dataclass(frozen=True)
class WireSegment:
    identity: str
    from_terminal_identity: str
    to_terminal_identity: str
    wire_tag: str
    conductor_size: str = ""
    color: str = ""
    circuit_function: str = ""
    conduit_identity: str = ""
    route: tuple[RoutePoint, ...] = ()
    specified_length_mm: float | None = None

    def validate(self) -> None:
        for value in (self.identity, self.from_terminal_identity, self.to_terminal_identity):
            if not is_ce_identity(value):
                raise ValueError(f"Invalid wire or terminal identity: {value}")
        if self.from_terminal_identity == self.to_terminal_identity:
            raise ValueError(f"Wire {self.identity} cannot connect a terminal to itself.")
        if not self.wire_tag.strip():
            raise ValueError(f"Wire {self.identity} requires a wire tag.")
        if self.specified_length_mm is not None and self.specified_length_mm < 0:
            raise ValueError(f"Wire {self.identity} cannot have a negative length.")

    @property
    def routed_length_mm(self) -> float | None:
        if len(self.route) < 2:
            return None
        return sum(
            math.dist(
                (start.x_mm, start.y_mm, start.z_mm),
                (end.x_mm, end.y_mm, end.z_mm),
            )
            for start, end in zip(self.route, self.route[1:])
        )

    @property
    def effective_length_mm(self) -> float | None:
        routed = self.routed_length_mm
        return routed if routed is not None else self.specified_length_mm


@dataclass(frozen=True)
class ElectricalConnectionPath:
    identity: str
    signal_identity: str
    signal_tag: str
    terminals: tuple[TerminalEndpoint, ...]
    wires: tuple[WireSegment, ...]

    def validate(self) -> None:
        if not is_ce_identity(self.identity):
            raise ValueError(f"Invalid connection-path identity: {self.identity}")
        if not is_ce_identity(self.signal_identity):
            raise ValueError(f"Invalid signal identity: {self.signal_identity}")
        if len(self.terminals) < 2:
            raise ValueError("A continuous connection path requires at least two terminals.")
        if len(self.wires) != len(self.terminals) - 1:
            raise ValueError("A continuous connection path requires one wire between each terminal pair.")

        identities = [self.identity, self.signal_identity]
        for terminal in self.terminals:
            terminal.validate()
            identities.append(terminal.identity)
        for index, wire in enumerate(self.wires):
            wire.validate()
            identities.append(wire.identity)
            if wire.from_terminal_identity != self.terminals[index].identity:
                raise ValueError(f"Wire {wire.identity} does not start at ordered terminal {index}.")
            if wire.to_terminal_identity != self.terminals[index + 1].identity:
                raise ValueError(f"Wire {wire.identity} does not end at ordered terminal {index + 1}.")
        if len(identities) != len(set(identities)):
            raise ValueError("Connection path contains duplicate CE identities.")
        if self.terminals[0].role != CERoles.PLC_CHANNEL_TERMINAL:
            raise ValueError("Connection path must start at a PLC channel terminal.")
        if self.terminals[-1].role != CERoles.DEVICE_TERMINAL:
            raise ValueError("Connection path must end at a field-device terminal.")

    @property
    def total_length_mm(self) -> float | None:
        lengths = [wire.effective_length_mm for wire in self.wires]
        if any(length is None for length in lengths):
            return None
        return sum(length for length in lengths if length is not None)


def serialize_connection_path(path: ElectricalConnectionPath) -> str:
    """Serialize a validated path using one fixed, deterministic contract."""

    path.validate()
    payload = {
        "format": PATH_FORMAT,
        "identity": path.identity,
        "signalIdentity": path.signal_identity,
        "signalTag": path.signal_tag,
        "terminals": [
            {
                "identity": terminal.identity,
                "role": terminal.role,
                "ownerIdentity": terminal.owner_identity,
                "designation": terminal.designation,
                "label": terminal.label,
            }
            for terminal in path.terminals
        ],
        "wires": [
            {
                "identity": wire.identity,
                "role": CERoles.WIRE,
                "fromTerminalIdentity": wire.from_terminal_identity,
                "toTerminalIdentity": wire.to_terminal_identity,
                "wireTag": wire.wire_tag,
                "conductorSize": wire.conductor_size,
                "color": wire.color,
                "circuitFunction": wire.circuit_function,
                "conduitIdentity": wire.conduit_identity,
                "route": [
                    {
                        "x_mm": float(point.x_mm),
                        "y_mm": float(point.y_mm),
                        "z_mm": float(point.z_mm),
                    }
                    for point in wire.route
                ],
                "specifiedLengthMm": (
                    float(wire.specified_length_mm)
                    if wire.specified_length_mm is not None
                    else None
                ),
                "routedLengthMm": wire.routed_length_mm,
            }
            for wire in path.wires
        ],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def deserialize_connection_path(serialized: str) -> ElectricalConnectionPath:
    """Read the fixed connection-path contract and reject other versions."""

    payload = json.loads(serialized)
    if payload.get("format") != PATH_FORMAT:
        raise ValueError(f"Unsupported connection-path format: {payload.get('format')}")
    path = ElectricalConnectionPath(
        identity=str(payload.get("identity", "")),
        signal_identity=str(payload.get("signalIdentity", "")),
        signal_tag=str(payload.get("signalTag", "")),
        terminals=tuple(
            TerminalEndpoint(
                identity=str(item.get("identity", "")),
                role=str(item.get("role", "")),
                owner_identity=str(item.get("ownerIdentity", "")),
                designation=str(item.get("designation", "")),
                label=str(item.get("label", "")),
            )
            for item in payload.get("terminals", [])
        ),
        wires=tuple(
            WireSegment(
                identity=str(item.get("identity", "")),
                from_terminal_identity=str(item.get("fromTerminalIdentity", "")),
                to_terminal_identity=str(item.get("toTerminalIdentity", "")),
                wire_tag=str(item.get("wireTag", "")),
                conductor_size=str(item.get("conductorSize", "")),
                color=str(item.get("color", "")),
                circuit_function=str(item.get("circuitFunction", "")),
                conduit_identity=str(item.get("conduitIdentity", "")),
                route=tuple(
                    RoutePoint(
                        x_mm=float(point["x_mm"]),
                        y_mm=float(point["y_mm"]),
                        z_mm=float(point["z_mm"]),
                    )
                    for point in item.get("route", [])
                ),
                specified_length_mm=(
                    float(item["specifiedLengthMm"])
                    if item.get("specifiedLengthMm") is not None
                    else None
                ),
            )
            for item in payload.get("wires", [])
        ),
    )
    path.validate()
    return path


def wiring_schedule_rows(path: ElectricalConnectionPath) -> list[dict[str, object]]:
    path.validate()
    rows = []
    for index, wire in enumerate(path.wires):
        start = path.terminals[index]
        end = path.terminals[index + 1]
        rows.append(
            {
                "PathIdentity": path.identity,
                "SignalIdentity": path.signal_identity,
                "SignalTag": path.signal_tag,
                "WireIdentity": wire.identity,
                "WireTag": wire.wire_tag,
                "ConductorSize": wire.conductor_size,
                "Color": wire.color,
                "CircuitFunction": wire.circuit_function,
                "ConduitIdentity": wire.conduit_identity,
                "FromTerminalIdentity": start.identity,
                "FromTerminal": start.designation,
                "ToTerminalIdentity": end.identity,
                "ToTerminal": end.designation,
                "LengthMm": wire.effective_length_mm,
            }
        )
    return rows


def io_schedule_row(path: ElectricalConnectionPath) -> dict[str, object]:
    path.validate()
    return {
        "PathIdentity": path.identity,
        "SignalIdentity": path.signal_identity,
        "SignalTag": path.signal_tag,
        "PLCTerminalIdentity": path.terminals[0].identity,
        "PLCTerminal": path.terminals[0].designation,
        "DeviceTerminalIdentity": path.terminals[-1].identity,
        "DeviceTerminal": path.terminals[-1].designation,
        "TerminalPath": " > ".join(terminal.designation for terminal in path.terminals),
        "WireTags": ";".join(wire.wire_tag for wire in path.wires),
        "TotalLengthMm": path.total_length_mm,
    }

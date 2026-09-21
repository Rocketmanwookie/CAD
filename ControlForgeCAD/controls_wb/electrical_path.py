# SPDX-License-Identifier: MIT
"""Continuous identity-safe terminal/wire paths and derived schedules."""

from __future__ import annotations

import json
import math
import csv
from dataclasses import dataclass
from io import StringIO
from xml.etree import ElementTree as ET

from controls_wb.identity import CERoles, is_ce_identity, validate_ce_role


PATH_FORMAT = "ceproject.connection-path/1.0"
PATH_XML_NAMESPACE = "https://whrsdaparty.github.io/ceproject/connection-path/1.0"
ET.register_namespace("cepath", PATH_XML_NAMESPACE)
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
        if self.route and len(self.route) < 2:
            raise ValueError(f"Wire {self.identity} route requires at least two points.")
        if any(
            not math.isfinite(coordinate)
            for point in self.route
            for coordinate in (point.x_mm, point.y_mm, point.z_mm)
        ):
            raise ValueError(f"Wire {self.identity} route coordinates must be finite.")
        if self.route and self.routed_length_mm <= 0:
            raise ValueError(f"Wire {self.identity} route must have a positive polyline length.")

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
                    float(_required_xml_attr(item, "specifiedLengthMm", "Wire"))
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


WIRING_SCHEDULE_HEADERS = (
    "PathIdentity", "SignalIdentity", "SignalTag", "WireIdentity", "WireTag",
    "FromTerminalIdentity", "FromTerminal", "ToTerminalIdentity", "ToTerminal",
    "ConductorSize", "Color", "CircuitFunction", "ConduitIdentity", "LengthMm",
)

IO_PATH_SCHEDULE_HEADERS = (
    "PathIdentity", "SignalIdentity", "SignalTag", "PLCTerminalIdentity",
    "PLCTerminal", "DeviceTerminalIdentity", "DeviceTerminal", "TerminalPath",
    "WireTags", "TotalLengthMm",
)


def wiring_schedule_csv(paths: tuple[ElectricalConnectionPath, ...]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=WIRING_SCHEDULE_HEADERS, lineterminator="\n")
    writer.writeheader()
    for path in sorted(paths, key=lambda item: (item.signal_tag, item.identity)):
        writer.writerows(wiring_schedule_rows(path))
    return output.getvalue()


def io_path_schedule_csv(paths: tuple[ElectricalConnectionPath, ...]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=IO_PATH_SCHEDULE_HEADERS, lineterminator="\n")
    writer.writeheader()
    for path in sorted(paths, key=lambda item: (item.signal_tag, item.identity)):
        writer.writerow(io_schedule_row(path))
    return output.getvalue()


def _xml_tag(name: str) -> str:
    return f"{{{PATH_XML_NAMESPACE}}}{name}"


def connection_path_to_xml(path: ElectricalConnectionPath) -> str:
    """Serialize one path as deterministic, namespace-correct XML."""

    path.validate()
    root = ET.Element(
        _xml_tag("ConnectionPath"),
        {
            "format": PATH_FORMAT,
            "identity": path.identity,
            "signalIdentity": path.signal_identity,
            "signalTag": path.signal_tag,
        },
    )
    terminals = ET.SubElement(root, _xml_tag("Terminals"))
    for sequence, terminal in enumerate(path.terminals):
        ET.SubElement(
            terminals,
            _xml_tag("Terminal"),
            {
                "sequence": str(sequence),
                "identity": terminal.identity,
                "role": terminal.role,
                "ownerIdentity": terminal.owner_identity,
                "designation": terminal.designation,
                "label": terminal.label,
            },
        )
    wires = ET.SubElement(root, _xml_tag("Wires"))
    for sequence, wire in enumerate(path.wires):
        attributes = {
            "sequence": str(sequence),
            "identity": wire.identity,
            "role": CERoles.WIRE,
            "fromTerminalIdentity": wire.from_terminal_identity,
            "toTerminalIdentity": wire.to_terminal_identity,
            "wireTag": wire.wire_tag,
            "conductorSize": wire.conductor_size,
            "color": wire.color,
            "circuitFunction": wire.circuit_function,
            "conduitIdentity": wire.conduit_identity,
        }
        if wire.specified_length_mm is not None:
            attributes["specifiedLengthMm"] = str(float(wire.specified_length_mm))
        if wire.routed_length_mm is not None:
            attributes["routedLengthMm"] = str(float(wire.routed_length_mm))
        wire_element = ET.SubElement(wires, _xml_tag("Wire"), attributes)
        if wire.route:
            route = ET.SubElement(wire_element, _xml_tag("Route"))
            for sequence_index, point in enumerate(wire.route):
                ET.SubElement(
                    route,
                    _xml_tag("Point"),
                    {
                        "sequence": str(sequence_index),
                        "xMm": str(float(point.x_mm)),
                        "yMm": str(float(point.y_mm)),
                        "zMm": str(float(point.z_mm)),
                    },
                )
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True, short_empty_elements=True)


def connection_path_from_xml(xml_text: str | bytes) -> ElectricalConnectionPath:
    """Parse the supported namespaced XML contract and validate graph semantics."""

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid connection-path XML: {exc}") from exc
    if root.tag != _xml_tag("ConnectionPath"):
        raise ValueError(f"Expected namespaced ConnectionPath root, found {root.tag}.")
    if root.get("format") != PATH_FORMAT:
        raise ValueError(f"Unsupported connection-path format: {root.get('format')}")
    terminals_parent = root.find(_xml_tag("Terminals"))
    wires_parent = root.find(_xml_tag("Wires"))
    if terminals_parent is None or wires_parent is None:
        raise ValueError("Connection-path XML requires Terminals and Wires.")

    terminal_elements = list(terminals_parent.findall(_xml_tag("Terminal")))
    wire_elements = list(wires_parent.findall(_xml_tag("Wire")))
    _require_contiguous_sequence(terminal_elements, "Terminal")
    _require_contiguous_sequence(wire_elements, "Wire")
    terminals = tuple(
        TerminalEndpoint(
            identity=_required_xml_attr(item, "identity", "Terminal"),
            role=_required_xml_attr(item, "role", "Terminal"),
            owner_identity=_required_xml_attr(item, "ownerIdentity", "Terminal"),
            designation=_required_xml_attr(item, "designation", "Terminal"),
            label=item.get("label", ""),
        )
        for item in terminal_elements
    )
    wires = []
    for item in wire_elements:
        if item.get("role") != CERoles.WIRE:
            raise ValueError(f"Wire requires role {CERoles.WIRE}.")
        route_element = item.find(_xml_tag("Route"))
        point_elements = [] if route_element is None else list(route_element.findall(_xml_tag("Point")))
        _require_contiguous_sequence(point_elements, "Point")
        wires.append(
            WireSegment(
                identity=_required_xml_attr(item, "identity", "Wire"),
                from_terminal_identity=_required_xml_attr(item, "fromTerminalIdentity", "Wire"),
                to_terminal_identity=_required_xml_attr(item, "toTerminalIdentity", "Wire"),
                wire_tag=_required_xml_attr(item, "wireTag", "Wire"),
                conductor_size=item.get("conductorSize", ""),
                color=item.get("color", ""),
                circuit_function=item.get("circuitFunction", ""),
                conduit_identity=item.get("conduitIdentity", ""),
                route=tuple(
                    RoutePoint(
                        float(_required_xml_attr(point, "xMm", "Point")),
                        float(_required_xml_attr(point, "yMm", "Point")),
                        float(_required_xml_attr(point, "zMm", "Point")),
                    )
                    for point in point_elements
                ),
                specified_length_mm=(
                    float(_required_xml_attr(item, "specifiedLengthMm", "Wire"))
                    if item.get("specifiedLengthMm") is not None
                    else None
                ),
            )
        )
    path = ElectricalConnectionPath(
        identity=_required_xml_attr(root, "identity", "ConnectionPath"),
        signal_identity=_required_xml_attr(root, "signalIdentity", "ConnectionPath"),
        signal_tag=_required_xml_attr(root, "signalTag", "ConnectionPath"),
        terminals=terminals,
        wires=tuple(wires),
    )
    path.validate()
    return path


def _required_xml_attr(element: ET.Element, name: str, context: str) -> str:
    value = element.get(name, "")
    if not value:
        raise ValueError(f"{context} requires {name}.")
    return value


def _require_contiguous_sequence(elements: list[ET.Element], context: str) -> None:
    for expected, element in enumerate(elements):
        if element.get("sequence") != str(expected):
            raise ValueError(f"{context} sequence must be contiguous from zero.")

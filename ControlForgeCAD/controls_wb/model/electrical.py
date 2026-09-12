# SPDX-License-Identifier: MIT
"""Typed FreeCAD document objects for continuous electrical paths."""

from __future__ import annotations

import json
from dataclasses import dataclass

from controls_wb.electrical_path import ElectricalConnectionPath, RoutePoint
from controls_wb.identity import CERoles, ensure_object_identity

try:
    import FreeCAD as App
    import Part
except Exception:  # pragma: no cover
    App = None
    Part = None


@dataclass(frozen=True)
class MaterializedElectricalPath:
    path_object: object
    terminal_objects: tuple[object, ...]
    wire_objects: tuple[object, ...]


def _add_property(obj, property_type: str, name: str, group: str, description: str) -> None:
    if name not in set(getattr(obj, "PropertiesList", []) or []):
        obj.addProperty(property_type, name, group, description)


def _identity_index(document) -> dict[str, object]:
    index = {}
    for obj in getattr(document, "Objects", []) or []:
        identity = str(getattr(obj, "CEIdentity", "") or "").strip()
        if not identity:
            continue
        if identity in index:
            raise ValueError(f"Document already contains duplicate CE identity {identity}.")
        index[identity] = obj
    return index


def _assert_identities_available(document, path: ElectricalConnectionPath) -> None:
    existing = _identity_index(document)
    requested = [path.identity]
    requested.extend(terminal.identity for terminal in path.terminals)
    requested.extend(wire.identity for wire in path.wires)
    collisions = sorted(identity for identity in requested if identity in existing)
    if collisions:
        raise ValueError(f"CE identities are already materialized: {', '.join(collisions)}")


def _route_json(route: tuple[RoutePoint, ...]) -> list[str]:
    return [
        json.dumps(
            {"sequence": index, "xMm": float(point.x_mm), "yMm": float(point.y_mm), "zMm": float(point.z_mm)},
            sort_keys=True,
            separators=(",", ":"),
        )
        for index, point in enumerate(route)
    ]


def materialize_electrical_path(document, path: ElectricalConnectionPath) -> MaterializedElectricalPath:
    """Create an ordered path and typed terminal/wire objects atomically at the caller boundary."""

    path.validate()
    _assert_identities_available(document, path)

    path_obj = document.addObject("App::FeaturePython", "CE_ConnectionPath")
    ElectricalPathObject(path_obj, path.identity)
    _add_property(path_obj, "App::PropertyString", "PathFormat", "Electrical Path", "Serialized path contract")
    _add_property(path_obj, "App::PropertyString", "SignalIdentity", "Electrical Path", "CE identity of signal")
    _add_property(path_obj, "App::PropertyString", "SignalTag", "Electrical Path", "Signal tag")
    _add_property(path_obj, "App::PropertyLinkList", "TerminalObjects", "Electrical Path", "Ordered terminal objects")
    _add_property(path_obj, "App::PropertyLinkList", "WireObjects", "Electrical Path", "Ordered wire objects")
    path_obj.PathFormat = "ceproject.connection-path/1.0"
    path_obj.SignalIdentity = path.signal_identity
    path_obj.SignalTag = path.signal_tag

    terminal_objects = []
    for terminal in path.terminals:
        obj = document.addObject("App::FeaturePython", "CE_Terminal")
        ElectricalTerminalObject(obj, terminal.role, terminal.identity)
        _add_property(obj, "App::PropertyString", "OwnerIdentity", "Electrical Terminal", "Owning device CE identity")
        _add_property(obj, "App::PropertyString", "Designation", "Electrical Terminal", "Terminal designation")
        _add_property(obj, "App::PropertyString", "TerminalLabel", "Electrical Terminal", "Terminal label")
        obj.OwnerIdentity = terminal.owner_identity
        obj.Designation = terminal.designation
        obj.TerminalLabel = terminal.label
        terminal_objects.append(obj)

    terminal_by_identity = {
        terminal.identity: obj for terminal, obj in zip(path.terminals, terminal_objects)
    }
    wire_objects = []
    for wire in path.wires:
        obj = document.addObject("Part::FeaturePython", "CE_Wire")
        ElectricalWireObject(obj, wire.identity)
        for property_type, name, description in (
            ("App::PropertyLink", "FromTerminal", "Starting terminal object"),
            ("App::PropertyLink", "ToTerminal", "Ending terminal object"),
            ("App::PropertyString", "FromTerminalIdentity", "Starting terminal CE identity"),
            ("App::PropertyString", "ToTerminalIdentity", "Ending terminal CE identity"),
            ("App::PropertyString", "WireTag", "Wire tag"),
            ("App::PropertyString", "ConductorSize", "Conductor size"),
            ("App::PropertyString", "Color", "Wire color"),
            ("App::PropertyString", "CircuitFunction", "Circuit function"),
            ("App::PropertyString", "ConduitIdentity", "Conduit or raceway CE identity"),
            ("App::PropertyStringList", "RoutePoints", "Ordered 3D route points in millimetres"),
            ("App::PropertyLength", "CalculatedLength", "Calculated or specified wire length"),
        ):
            _add_property(obj, property_type, name, "Electrical Wire", description)
        obj.FromTerminal = terminal_by_identity[wire.from_terminal_identity]
        obj.ToTerminal = terminal_by_identity[wire.to_terminal_identity]
        obj.FromTerminalIdentity = wire.from_terminal_identity
        obj.ToTerminalIdentity = wire.to_terminal_identity
        obj.WireTag = wire.wire_tag
        obj.ConductorSize = wire.conductor_size
        obj.Color = wire.color
        obj.CircuitFunction = wire.circuit_function
        obj.ConduitIdentity = wire.conduit_identity
        obj.RoutePoints = _route_json(wire.route)
        obj.CalculatedLength = f"{wire.effective_length_mm or 0.0} mm"
        wire_objects.append(obj)

    path_obj.TerminalObjects = terminal_objects
    path_obj.WireObjects = wire_objects
    return MaterializedElectricalPath(path_obj, tuple(terminal_objects), tuple(wire_objects))


class ElectricalPathObject:
    def __init__(self, obj, identity: str):
        obj.Proxy = self
        self.Type = "ElectricalPathObject"
        ensure_object_identity(obj, CERoles.CONNECTION_PATH, identity)

    def execute(self, obj):
        return None

    def onDocumentRestored(self, obj):
        ensure_object_identity(obj, CERoles.CONNECTION_PATH, getattr(obj, "CEIdentity", ""))


class ElectricalTerminalObject:
    def __init__(self, obj, role: str, identity: str):
        obj.Proxy = self
        self.Type = "ElectricalTerminalObject"
        self.Role = role
        ensure_object_identity(obj, role, identity)

    def execute(self, obj):
        return None

    def onDocumentRestored(self, obj):
        ensure_object_identity(obj, self.Role, getattr(obj, "CEIdentity", ""))


class ElectricalWireObject:
    def __init__(self, obj, identity: str):
        obj.Proxy = self
        self.Type = "ElectricalWireObject"
        ensure_object_identity(obj, CERoles.WIRE, identity)

    def execute(self, obj):
        route = _route_from_object(obj)
        if Part is not None and App is not None and len(route) >= 2:
            obj.Shape = Part.makePolygon([App.Vector(point.x_mm, point.y_mm, point.z_mm) for point in route])

    def onDocumentRestored(self, obj):
        ensure_object_identity(obj, CERoles.WIRE, getattr(obj, "CEIdentity", ""))


def _route_from_object(obj) -> tuple[RoutePoint, ...]:
    points = []
    for record in getattr(obj, "RoutePoints", []) or []:
        payload = json.loads(record)
        points.append(
            (int(payload["sequence"]), RoutePoint(float(payload["xMm"]), float(payload["yMm"]), float(payload["zMm"])))
        )
    points.sort(key=lambda item: item[0])
    if [sequence for sequence, _ in points] != list(range(len(points))):
        raise ValueError("Wire route point sequence must be contiguous from zero.")
    return tuple(point for _, point in points)

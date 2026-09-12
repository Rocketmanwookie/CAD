# SPDX-License-Identifier: MIT
"""Typed FreeCAD document objects for continuous electrical paths."""

from __future__ import annotations

import json
from dataclasses import dataclass

from controls_wb.electrical_path import ElectricalConnectionPath, RoutePoint
from controls_wb.identity import CERoles, ensure_object_identity, is_ce_identity, new_ce_identity

try:
    import FreeCAD as App
    import Part
except Exception:  # pragma: no cover
    App = None
    Part = None


@dataclass(frozen=True)
class MaterializedElectricalPath:
    path_object: object
    signal_object: object
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


def _assert_identities_available(document, path: ElectricalConnectionPath) -> dict[str, object]:
    existing = _identity_index(document)
    requested = [path.identity]
    requested.extend(terminal.identity for terminal in path.terminals)
    requested.extend(wire.identity for wire in path.wires)
    collisions = sorted(identity for identity in requested if identity in existing)
    if collisions:
        raise ValueError(f"CE identities are already materialized: {', '.join(collisions)}")
    return existing


def _project_object(document):
    for obj in getattr(document, "Objects", []) or []:
        if getattr(obj, "CERole", "") == CERoles.PROJECT or hasattr(obj, "ProjectId"):
            return obj
    return None


def _append_unique_link(obj, property_name: str, linked_obj) -> None:
    links = list(getattr(obj, property_name, []) or [])
    if linked_obj not in links:
        links.append(linked_obj)
        setattr(obj, property_name, links)


def register_electrical_device(project, device) -> None:
    """Register one already-identified physical occurrence on a CE project."""

    identity = str(getattr(device, "CEIdentity", "") or "")
    role = str(getattr(device, "CERole", "") or "")
    if not is_ce_identity(identity):
        raise ValueError("Electrical device registration requires a valid CE identity.")
    if role in {"", CERoles.PROJECT, CERoles.SIGNAL, CERoles.WIRE, CERoles.CONNECTION_PATH}:
        raise ValueError(f"Role {role!r} is not an electrical device occurrence role.")
    _add_property(project, "App::PropertyLinkList", "ElectricalDevices", "Electrical Graph", "Typed electrical device occurrences owned by this project")
    _append_unique_link(project, "ElectricalDevices", device)


def materialize_electrical_device(
    document,
    tag: str,
    *,
    role: str = CERoles.FIELD_DEVICE,
    identity: str | None = None,
    manufacturer: str = "",
    part_number: str = "",
    description: str = "",
):
    """Create and immediately identify/register a typed electrical occurrence."""

    clean_tag = str(tag).strip()
    if not clean_tag:
        raise ValueError("Electrical device requires a tag.")
    candidate_identity = identity or new_ce_identity()
    if candidate_identity in _identity_index(document):
        raise ValueError(f"CE identity is already materialized: {candidate_identity}")
    obj = document.addObject("App::FeaturePython", "CE_Device")
    ElectricalDeviceObject(obj, role, candidate_identity)
    for name, value, description_text in (
        ("Tag", clean_tag, "Device tag"),
        ("Manufacturer", manufacturer, "Manufacturer"),
        ("PartNumber", part_number, "Part number"),
        ("Description", description, "Device description"),
    ):
        _add_property(obj, "App::PropertyString", name, "Electrical Device", description_text)
        setattr(obj, name, value)
    project = _project_object(document)
    if project is not None:
        register_electrical_device(project, obj)
    return obj


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
    existing = _assert_identities_available(document, path)

    signal_obj = existing.get(path.signal_identity)
    if signal_obj is not None:
        if getattr(signal_obj, "CERole", "") != CERoles.SIGNAL:
            raise ValueError(f"Signal identity {path.signal_identity} belongs to a non-signal object.")
        existing_tag = str(getattr(signal_obj, "SignalTag", "") or "")
        if existing_tag and existing_tag != path.signal_tag:
            raise ValueError(f"Signal identity {path.signal_identity} has conflicting tags.")
    else:
        signal_obj = document.addObject("App::FeaturePython", "CE_Signal")
        ElectricalSignalObject(signal_obj, path.signal_identity)
        _add_property(signal_obj, "App::PropertyString", "SignalTag", "Electrical Signal", "Signal tag")
        _add_property(signal_obj, "App::PropertyLinkList", "ConnectionPaths", "Electrical Signal", "Paths carrying this signal")
        signal_obj.SignalTag = path.signal_tag

    path_obj = document.addObject("App::FeaturePython", "CE_ConnectionPath")
    ElectricalPathObject(path_obj, path.identity)
    _add_property(path_obj, "App::PropertyString", "PathFormat", "Electrical Path", "Serialized path contract")
    _add_property(path_obj, "App::PropertyString", "SignalIdentity", "Electrical Path", "CE identity of signal")
    _add_property(path_obj, "App::PropertyString", "SignalTag", "Electrical Path", "Signal tag")
    _add_property(path_obj, "App::PropertyLink", "SignalObject", "Electrical Path", "Typed signal object")
    _add_property(path_obj, "App::PropertyLinkList", "TerminalObjects", "Electrical Path", "Ordered terminal objects")
    _add_property(path_obj, "App::PropertyLinkList", "WireObjects", "Electrical Path", "Ordered wire objects")
    path_obj.PathFormat = "ceproject.connection-path/1.0"
    path_obj.SignalIdentity = path.signal_identity
    path_obj.SignalTag = path.signal_tag
    path_obj.SignalObject = signal_obj

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
            ("App::PropertyBool", "HasSpecifiedLength", "Whether a separate specified wire length was provided"),
            ("App::PropertyLength", "SpecifiedLength", "Specified wire length before route calculation"),
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
        obj.HasSpecifiedLength = wire.specified_length_mm is not None
        obj.SpecifiedLength = f"{wire.specified_length_mm or 0.0} mm"
        obj.CalculatedLength = f"{wire.effective_length_mm or 0.0} mm"
        wire_objects.append(obj)

    path_obj.TerminalObjects = terminal_objects
    path_obj.WireObjects = wire_objects
    _append_unique_link(signal_obj, "ConnectionPaths", path_obj)
    project = _project_object(document)
    if project is not None:
        _add_property(project, "App::PropertyLinkList", "ElectricalSignals", "Electrical Graph", "Typed signal objects owned by this project")
        _add_property(project, "App::PropertyLinkList", "ElectricalPaths", "Electrical Graph", "Typed continuous connection paths owned by this project")
        _add_property(project, "App::PropertyLinkList", "ElectricalDevices", "Electrical Graph", "Typed electrical device occurrences owned by this project")
        _append_unique_link(project, "ElectricalSignals", signal_obj)
        _append_unique_link(project, "ElectricalPaths", path_obj)
    return MaterializedElectricalPath(path_obj, signal_obj, tuple(terminal_objects), tuple(wire_objects))


class ElectricalPathObject:
    def __init__(self, obj, identity: str):
        obj.Proxy = self
        self.Type = "ElectricalPathObject"
        ensure_object_identity(obj, CERoles.CONNECTION_PATH, identity)

    def execute(self, obj):
        return None

    def onDocumentRestored(self, obj):
        ensure_object_identity(obj, CERoles.CONNECTION_PATH, getattr(obj, "CEIdentity", ""))


class ElectricalSignalObject:
    def __init__(self, obj, identity: str):
        obj.Proxy = self
        self.Type = "ElectricalSignalObject"
        ensure_object_identity(obj, CERoles.SIGNAL, identity)

    def execute(self, obj):
        return None

    def onDocumentRestored(self, obj):
        ensure_object_identity(obj, CERoles.SIGNAL, getattr(obj, "CEIdentity", ""))


class ElectricalDeviceObject:
    def __init__(self, obj, role: str, identity: str):
        obj.Proxy = self
        self.Type = "ElectricalDeviceObject"
        self.Role = role
        ensure_object_identity(obj, role, identity)

    def execute(self, obj):
        return None

    def onDocumentRestored(self, obj):
        ensure_object_identity(obj, self.Role, getattr(obj, "CEIdentity", ""))


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


def electrical_path_from_object(path_obj) -> ElectricalConnectionPath:
    """Reconstruct and validate a domain path from typed FreeCAD links."""

    signal_obj = getattr(path_obj, "SignalObject", None)
    signal_identity = str(getattr(path_obj, "SignalIdentity", "") or "")
    if signal_obj is None or getattr(signal_obj, "CEIdentity", "") != signal_identity:
        raise ValueError(f"Path {getattr(path_obj, 'CEIdentity', '')} has a broken signal-object link.")
    terminals = tuple(
        _terminal_from_object(obj) for obj in (getattr(path_obj, "TerminalObjects", []) or [])
    )
    wires = tuple(_wire_from_object(obj) for obj in (getattr(path_obj, "WireObjects", []) or []))
    path = ElectricalConnectionPath(
        identity=str(getattr(path_obj, "CEIdentity", "") or ""),
        signal_identity=signal_identity,
        signal_tag=str(getattr(path_obj, "SignalTag", "") or ""),
        terminals=terminals,
        wires=wires,
    )
    path.validate()
    for wire_obj, wire in zip(getattr(path_obj, "WireObjects", []) or [], wires):
        if getattr(getattr(wire_obj, "FromTerminal", None), "CEIdentity", "") != wire.from_terminal_identity:
            raise ValueError(f"Wire {wire.identity} has a broken FromTerminal link.")
        if getattr(getattr(wire_obj, "ToTerminal", None), "CEIdentity", "") != wire.to_terminal_identity:
            raise ValueError(f"Wire {wire.identity} has a broken ToTerminal link.")
    return path


def electrical_paths_from_project(project) -> tuple[ElectricalConnectionPath, ...]:
    return tuple(
        electrical_path_from_object(obj)
        for obj in (getattr(project, "ElectricalPaths", []) or [])
    )


def update_electrical_path_object(path_obj, updated: ElectricalConnectionPath):
    """Apply editable path fields while requiring every persisted identity to remain fixed."""

    current = electrical_path_from_object(path_obj)
    current_identities = (
        current.identity,
        current.signal_identity,
        *(terminal.identity for terminal in current.terminals),
        *(wire.identity for wire in current.wires),
    )
    updated_identities = (
        updated.identity,
        updated.signal_identity,
        *(terminal.identity for terminal in updated.terminals),
        *(wire.identity for wire in updated.wires),
    )
    if current_identities != updated_identities:
        raise ValueError("Electrical path editing cannot change path, signal, terminal, or wire identities.")
    updated.validate()
    signal_obj = path_obj.SignalObject
    document = getattr(path_obj, "Document", None)
    for obj in getattr(document, "Objects", []) or []:
        if (
            obj is not signal_obj
            and getattr(obj, "CERole", "") == CERoles.SIGNAL
            and getattr(obj, "SignalTag", "") == updated.signal_tag
        ):
            raise ValueError(f"Another signal already uses tag {updated.signal_tag}.")
    signal_obj.SignalTag = updated.signal_tag
    for linked_path in getattr(signal_obj, "ConnectionPaths", []) or []:
        if getattr(linked_path, "SignalIdentity", "") == updated.signal_identity:
            linked_path.SignalTag = updated.signal_tag
    for obj, terminal in zip(path_obj.TerminalObjects, updated.terminals):
        obj.Designation = terminal.designation
        obj.TerminalLabel = terminal.label
    for obj, wire in zip(path_obj.WireObjects, updated.wires):
        obj.WireTag = wire.wire_tag
        obj.ConductorSize = wire.conductor_size
        obj.Color = wire.color
        obj.CircuitFunction = wire.circuit_function
        obj.ConduitIdentity = wire.conduit_identity
        obj.RoutePoints = _route_json(wire.route)
        obj.HasSpecifiedLength = wire.specified_length_mm is not None
        obj.SpecifiedLength = f"{wire.specified_length_mm or 0.0} mm"
        obj.CalculatedLength = f"{wire.effective_length_mm or 0.0} mm"
        execute = getattr(getattr(obj, "Proxy", None), "execute", None)
        if callable(execute):
            execute(obj)
    return path_obj


def _terminal_from_object(obj):
    from controls_wb.electrical_path import TerminalEndpoint

    return TerminalEndpoint(
        identity=str(getattr(obj, "CEIdentity", "") or ""),
        role=str(getattr(obj, "CERole", "") or ""),
        owner_identity=str(getattr(obj, "OwnerIdentity", "") or ""),
        designation=str(getattr(obj, "Designation", "") or ""),
        label=str(getattr(obj, "TerminalLabel", "") or ""),
    )


def _wire_from_object(obj):
    from controls_wb.electrical_path import WireSegment

    route = _route_from_object(obj)
    if hasattr(obj, "HasSpecifiedLength"):
        specified_length = (
            _length_mm(getattr(obj, "SpecifiedLength", None))
            if getattr(obj, "HasSpecifiedLength", False)
            else None
        )
    else:
        # Compatibility with path objects created before separate length storage.
        specified_length = None if route else _length_mm(getattr(obj, "CalculatedLength", None))
    return WireSegment(
        identity=str(getattr(obj, "CEIdentity", "") or ""),
        from_terminal_identity=str(getattr(obj, "FromTerminalIdentity", "") or ""),
        to_terminal_identity=str(getattr(obj, "ToTerminalIdentity", "") or ""),
        wire_tag=str(getattr(obj, "WireTag", "") or ""),
        conductor_size=str(getattr(obj, "ConductorSize", "") or ""),
        color=str(getattr(obj, "Color", "") or ""),
        circuit_function=str(getattr(obj, "CircuitFunction", "") or ""),
        conduit_identity=str(getattr(obj, "ConduitIdentity", "") or ""),
        route=route,
        specified_length_mm=specified_length,
    )


def _length_mm(value) -> float | None:
    if value is None:
        return None
    numeric = getattr(value, "Value", value)
    if isinstance(numeric, str):
        numeric = numeric.removesuffix(" mm").strip()
    try:
        return float(numeric)
    except (TypeError, ValueError):
        return None

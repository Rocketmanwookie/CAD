# SPDX-License-Identifier: MIT
"""User-facing continuous electrical-path form and pure normalization helpers."""

from __future__ import annotations

import math
from dataclasses import replace

from controls_wb.electrical_path import ElectricalConnectionPath, RoutePoint, TerminalEndpoint, WireSegment
from controls_wb.gui.io_signal import _qt_widgets
from controls_wb.gui.project_intake import existing_project_object
from controls_wb.identity import CERoles, new_ce_identity
from controls_wb.model.electrical import (
    electrical_path_from_object,
    materialize_electrical_device,
    materialize_electrical_path,
    update_electrical_path_object,
)
from controls_wb.model.project import create_or_update_project
from controls_wb.wire_engineering import standardized_wire_color


def _devices_for_role(project, role: str) -> list[object]:
    return [
        device for device in (getattr(project, "ElectricalDevices", []) or [])
        if getattr(device, "CERole", "") == role
    ]


def _device_by_identity(project, identity: str, expected_role: str):
    for device in _devices_for_role(project, expected_role):
        if getattr(device, "CEIdentity", "") == identity:
            return device
    raise ValueError(f"No registered {expected_role} device has identity {identity}.")


def _positive_length(value: object, label: str) -> float:
    try:
        length = float(str(value).strip())
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a numeric millimetre length.") from exc
    if length <= 0:
        raise ValueError(f"{label} must be greater than zero.")
    return length


def parse_route_points(value: object, label: str) -> tuple[RoutePoint, ...]:
    """Parse ``x,y,z; x,y,z`` millimetre coordinates from a form field."""

    text = str(value or "").strip()
    if not text:
        return ()
    points = []
    for position, record in enumerate(text.split(";"), start=1):
        coordinates = [item.strip() for item in record.split(",")]
        if len(coordinates) != 3:
            raise ValueError(f"{label} point {position} must contain x,y,z coordinates.")
        try:
            x_mm, y_mm, z_mm = (float(item) for item in coordinates)
        except ValueError as exc:
            raise ValueError(f"{label} point {position} coordinates must be numeric.") from exc
        if not all(math.isfinite(item) for item in (x_mm, y_mm, z_mm)):
            raise ValueError(f"{label} point {position} coordinates must be finite.")
        points.append(RoutePoint(x_mm, y_mm, z_mm))
    if len(points) < 2:
        raise ValueError(f"{label} requires at least two route points when provided.")
    return tuple(points)


def _specified_length(value: object, label: str, route: tuple[RoutePoint, ...]) -> float | None:
    if str(value or "").strip():
        return _positive_length(value, label)
    if not route:
        raise ValueError(f"{label} is required when no 3D route is provided.")
    return None


def _build_electrical_path(
    project,
    values: dict[str, str],
    *,
    plc_identity: str,
    terminal_strip_identity: str,
    device_identity: str,
) -> ElectricalConnectionPath:
    signal_tag = str(values.get("signal_tag", "")).strip()
    if not signal_tag:
        raise ValueError("Signal tag is required.")
    conductor_size = str(values.get("conductor_size", "")).strip()
    if not conductor_size:
        raise ValueError("Conductor size is required.")
    circuit_function = str(values.get("circuit_function", "")).strip().lower()
    requested_color = str(values.get("color", "")).strip()
    color = standardized_wire_color(
        circuit_function,
        {circuit_function: requested_color} if requested_color else None,
    )
    signal_identity = ""
    for signal in (getattr(project, "ElectricalSignals", []) or []):
        if getattr(signal, "SignalTag", "") == signal_tag:
            signal_identity = str(getattr(signal, "CEIdentity"))
            break
    signal_identity = signal_identity or new_ce_identity()
    terminals = (
        TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, plc_identity, str(values.get("plc_terminal", "")).strip()),
        TerminalEndpoint(new_ce_identity(), CERoles.CABINET_TERMINAL, terminal_strip_identity, str(values.get("terminal_in", "")).strip()),
        TerminalEndpoint(new_ce_identity(), CERoles.CABINET_TERMINAL, terminal_strip_identity, str(values.get("terminal_out", "")).strip()),
        TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, device_identity, str(values.get("device_terminal", "")).strip()),
    )
    wire_tags = [str(values.get(f"wire_{index}_tag", "")).strip() for index in range(1, 4)]
    if any(not tag for tag in wire_tags):
        raise ValueError("All three wire/jumper tags are required.")
    routes = [
        parse_route_points(values.get(f"wire_{index}_route_mm", ""), f"Wire {index} route")
        for index in range(1, 4)
    ]
    lengths = [
        _specified_length(
            values.get(f"wire_{index}_length_mm", ""),
            f"Wire {index} length",
            routes[index - 1],
        )
        for index in range(1, 4)
    ]
    wires = tuple(
        WireSegment(
            new_ce_identity(), terminals[index].identity, terminals[index + 1].identity, wire_tags[index],
            conductor_size=conductor_size,
            color=color,
            circuit_function=circuit_function,
            route=routes[index],
            specified_length_mm=lengths[index],
        )
        for index in range(3)
    )
    path = ElectricalConnectionPath(new_ce_identity(), signal_identity, signal_tag, terminals, wires)
    path.validate()
    return path


def build_electrical_path(project, values: dict[str, str]) -> ElectricalConnectionPath:
    """Normalize form values into a validated continuous path without FreeCAD APIs."""

    channel = _device_by_identity(project, values.get("plc_channel_identity", ""), CERoles.PLC_CHANNEL)
    signal = getattr(channel, "AllocatedSignalObject", None)
    if signal is None or getattr(signal, "CERole", "") != CERoles.SIGNAL:
        raise ValueError("Selected PLC channel has no typed allocated signal.")
    signal_tag = str(getattr(signal, "SignalTag", "") or "")
    if str(values.get("signal_tag", "")).strip() != signal_tag:
        raise ValueError("Signal tag must match the selected allocated PLC channel.")
    designation = str(getattr(channel, "SignalAddress", "") or "")
    if not designation:
        raise ValueError("Selected PLC channel has no allocated address for its terminal designation.")
    requested_designation = str(values.get("plc_terminal", "")).strip()
    if requested_designation and requested_designation != designation:
        raise ValueError("PLC terminal designation must match the selected allocated channel address.")
    strip = _device_by_identity(project, values.get("terminal_strip_identity", ""), CERoles.TERMINAL_STRIP)
    device = _device_by_identity(project, values.get("device_owner_identity", ""), CERoles.FIELD_DEVICE)
    normalized = dict(values, plc_terminal=designation, signal_tag=signal_tag)
    return _build_electrical_path(
        project,
        normalized,
        plc_identity=channel.CEIdentity,
        terminal_strip_identity=strip.CEIdentity,
        device_identity=device.CEIdentity,
    )


def add_electrical_path_from_form(document, values: dict[str, str]):
    project = existing_project_object(document) or create_or_update_project(document)
    normalized = dict(values)
    channel = _device_by_identity(project, normalized.get("plc_channel_identity", ""), CERoles.PLC_CHANNEL)
    signal = getattr(channel, "AllocatedSignalObject", None)
    if signal is None or getattr(signal, "CERole", "") != CERoles.SIGNAL:
        raise ValueError("Selected PLC channel has no typed allocated signal.")
    signal_tag = str(getattr(signal, "SignalTag", "") or "")
    if str(normalized.get("signal_tag", "")).strip() != signal_tag:
        raise ValueError("Signal tag must match the selected allocated PLC channel.")
    designation = str(getattr(channel, "SignalAddress", "") or "")
    if not designation:
        raise ValueError("Selected PLC channel has no allocated address for its terminal designation.")
    requested_designation = str(normalized.get("plc_terminal", "")).strip()
    if requested_designation and requested_designation != designation:
        raise ValueError("PLC terminal designation must match the selected allocated channel address.")
    normalized["signal_tag"] = signal_tag
    normalized["plc_terminal"] = designation
    strip = _device_by_identity(project, normalized.get("terminal_strip_identity", ""), CERoles.TERMINAL_STRIP)
    device_identity = str(normalized.get("device_owner_identity", "")).strip()
    new_device_identity = ""
    if device_identity:
        device = _device_by_identity(project, device_identity, CERoles.FIELD_DEVICE)
        device_identity = device.CEIdentity
    else:
        if not str(normalized.get("device_tag", "")).strip():
            raise ValueError("Select an existing field device or enter a new field-device tag.")
        new_device_identity = new_ce_identity()
        device_identity = new_device_identity
    path = _build_electrical_path(
        project,
        normalized,
        plc_identity=channel.CEIdentity,
        terminal_strip_identity=strip.CEIdentity,
        device_identity=device_identity,
    )
    if new_device_identity:
        device = materialize_electrical_device(
            document,
            normalized.get("device_tag", ""),
            identity=new_device_identity,
            description=normalized.get("device_description", ""),
        )
    return materialize_electrical_path(document, path)


def update_electrical_path_from_form(path: ElectricalConnectionPath, values: dict[str, str]):
    """Build an edited path while preserving every graph identity and topology link."""

    if len(path.terminals) != 4 or len(path.wires) != 3:
        raise ValueError("The current path editor supports the fixed four-terminal, three-wire topology.")
    signal_tag = str(values.get("signal_tag", "")).strip()
    if not signal_tag:
        raise ValueError("Signal tag is required.")
    conductor_size = str(values.get("conductor_size", "")).strip()
    if not conductor_size:
        raise ValueError("Conductor size is required.")
    circuit_function = str(values.get("circuit_function", "")).strip().lower()
    requested_color = str(values.get("color", "")).strip()
    color = standardized_wire_color(
        circuit_function,
        {circuit_function: requested_color} if requested_color else None,
    )
    designations = [
        str(values.get(name, "")).strip()
        for name in ("plc_terminal", "terminal_in", "terminal_out", "device_terminal")
    ]
    terminals = tuple(
        replace(terminal, designation=designation)
        for terminal, designation in zip(path.terminals, designations)
    )
    wires = []
    for index, wire in enumerate(path.wires, start=1):
        route = parse_route_points(values.get(f"wire_{index}_route_mm", ""), f"Wire {index} route")
        wires.append(
            replace(
                wire,
                wire_tag=str(values.get(f"wire_{index}_tag", "")).strip(),
                conductor_size=conductor_size,
                color=color,
                circuit_function=circuit_function,
                route=route,
                specified_length_mm=_specified_length(
                    values.get(f"wire_{index}_length_mm", ""), f"Wire {index} length", route
                ),
            )
        )
    updated = replace(path, signal_tag=signal_tag, terminals=terminals, wires=tuple(wires))
    updated.validate()
    return updated


def _route_text(route: tuple[RoutePoint, ...]) -> str:
    return "; ".join(f"{point.x_mm:g},{point.y_mm:g},{point.z_mm:g}" for point in route)


def edit_electrical_path_from_form(path_obj, values: dict[str, str]):
    """Apply an edit while preserving an allocated channel's terminal contract."""

    current = electrical_path_from_object(path_obj)
    owner_identity = current.terminals[0].owner_identity
    channel = next(
        (
            obj for obj in (getattr(getattr(path_obj, "Document", None), "Objects", []) or [])
            if getattr(obj, "CEIdentity", "") == owner_identity
            and getattr(obj, "CERole", "") == CERoles.PLC_CHANNEL
        ),
        None,
    )
    normalized = dict(values)
    if channel is not None:
        allocated_designation = str(getattr(channel, "SignalAddress", "") or "")
        requested_designation = str(normalized.get("plc_terminal", "")).strip()
        if requested_designation != allocated_designation:
            raise ValueError("PLC terminal designation must remain the allocated channel address.")
        normalized["plc_terminal"] = allocated_designation
    return update_electrical_path_object(path_obj, update_electrical_path_from_form(current, normalized))


def _add_device_items(combo, devices: list[object]) -> None:
    for device in devices:
        label = f"{getattr(device, 'Tag', getattr(device, 'Name', 'Device'))} — {getattr(device, 'CERole', '')}"
        combo.addItem(label, getattr(device, "CEIdentity", ""))


def _combo_identity(combo) -> str:
    current_data = getattr(combo, "currentData", None)
    if callable(current_data):
        return str(current_data() or "")
    return str(combo.itemData(combo.currentIndex()) or "")


def show_electrical_path_dialog(document, parent=None, console=None):
    QtWidgets = _qt_widgets()
    project = existing_project_object(document) or create_or_update_project(document)
    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Add Continuous Electrical Path")
    layout = QtWidgets.QVBoxLayout(dialog)
    form = QtWidgets.QFormLayout()
    plc_combo = QtWidgets.QComboBox()
    strip_combo = QtWidgets.QComboBox()
    device_combo = QtWidgets.QComboBox()
    _add_device_items(plc_combo, _devices_for_role(project, CERoles.PLC_CHANNEL))
    _add_device_items(strip_combo, _devices_for_role(project, CERoles.TERMINAL_STRIP))
    device_combo.addItem("Create new field device…", "")
    _add_device_items(device_combo, _devices_for_role(project, CERoles.FIELD_DEVICE))
    form.addRow("Allocated PLC channel", plc_combo)
    form.addRow("Terminal strip", strip_combo)
    form.addRow("Existing field device", device_combo)
    editors = {}
    for key, label, default in (
        ("device_tag", "New field-device tag", ""),
        ("device_description", "New device description", ""),
        ("signal_tag", "Signal tag", "DI-0001"),
        ("plc_terminal", "PLC channel terminal (derived from allocation)", ""),
        ("terminal_in", "Cabinet terminal input", "TB1:1-IN"),
        ("terminal_out", "Cabinet terminal output", "TB1:1-OUT"),
        ("device_terminal", "Device terminal", "1"),
        ("conductor_size", "Conductor size", "18 AWG"),
        ("color", "Approved wire color", "blue"),
        ("circuit_function", "Circuit function", "dc_control"),
        ("wire_1_tag", "PLC-to-terminal wire", "W-001"),
        ("wire_1_length_mm", "PLC wire length (mm)", "100"),
        ("wire_1_route_mm", "PLC wire 3D route (x,y,z; … mm)", ""),
        ("wire_2_tag", "Terminal bridge/jumper", "JMP-001"),
        ("wire_2_length_mm", "Jumper length (mm)", "25"),
        ("wire_2_route_mm", "Jumper 3D route (x,y,z; … mm)", ""),
        ("wire_3_tag", "Terminal-to-device wire", "W-002"),
        ("wire_3_length_mm", "Field wire length (mm)", "1000"),
        ("wire_3_route_mm", "Field wire 3D route (x,y,z; … mm)", ""),
    ):
        editor = QtWidgets.QLineEdit()
        editor.setText(default)
        editors[key] = editor
        form.addRow(label, editor)
    layout.addLayout(form)
    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    execute = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if execute() != QtWidgets.QDialog.Accepted:
        return None
    values = {key: editor.text() for key, editor in editors.items()}
    values.update(
        plc_channel_identity=_combo_identity(plc_combo),
        terminal_strip_identity=_combo_identity(strip_combo),
        device_owner_identity=_combo_identity(device_combo),
    )
    result = add_electrical_path_from_form(document, values)
    if console is not None:
        console.PrintMessage(f"Electrical path added: {result.path_object.SignalTag}\n")
    return result


def show_edit_electrical_path_dialog(path_obj, parent=None, console=None):
    """Edit engineering fields on the selected fixed-topology path."""

    QtWidgets = _qt_widgets()
    path = electrical_path_from_object(path_obj)
    if len(path.terminals) != 4 or len(path.wires) != 3:
        raise ValueError("The current path editor supports the fixed four-terminal, three-wire topology.")
    defaults = {
        "signal_tag": path.signal_tag,
        "plc_terminal": path.terminals[0].designation,
        "terminal_in": path.terminals[1].designation,
        "terminal_out": path.terminals[2].designation,
        "device_terminal": path.terminals[3].designation,
        "conductor_size": path.wires[0].conductor_size,
        "color": path.wires[0].color,
        "circuit_function": path.wires[0].circuit_function,
    }
    for index, wire in enumerate(path.wires, start=1):
        defaults[f"wire_{index}_tag"] = wire.wire_tag
        defaults[f"wire_{index}_length_mm"] = (
            "" if wire.specified_length_mm is None else f"{wire.specified_length_mm:g}"
        )
        defaults[f"wire_{index}_route_mm"] = _route_text(wire.route)
    labels = {
        "signal_tag": "Signal tag",
        "plc_terminal": "PLC channel terminal",
        "terminal_in": "Cabinet terminal input",
        "terminal_out": "Cabinet terminal output",
        "device_terminal": "Device terminal",
        "conductor_size": "Conductor size",
        "color": "Approved wire color",
        "circuit_function": "Circuit function",
    }
    for index, segment in enumerate(("PLC wire", "Jumper", "Field wire"), start=1):
        labels[f"wire_{index}_tag"] = f"{segment} tag"
        labels[f"wire_{index}_length_mm"] = f"{segment} specified length (mm)"
        labels[f"wire_{index}_route_mm"] = f"{segment} 3D route (x,y,z; … mm)"
    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle(f"Edit Electrical Path — {path.signal_tag}")
    layout = QtWidgets.QVBoxLayout(dialog)
    form = QtWidgets.QFormLayout()
    editors = {}
    for key, value in defaults.items():
        editor = QtWidgets.QLineEdit()
        editor.setText(value)
        editors[key] = editor
        form.addRow(labels[key], editor)
    layout.addLayout(form)
    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    execute = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if execute() != QtWidgets.QDialog.Accepted:
        return None
    result = edit_electrical_path_from_form(
        path_obj, {key: editor.text() for key, editor in editors.items()}
    )
    if console is not None:
        console.PrintMessage(f"Electrical path updated: {result.SignalTag}\n")
    return result

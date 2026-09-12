# SPDX-License-Identifier: MIT
"""User-facing continuous electrical-path form and pure normalization helpers."""

from __future__ import annotations

import math

from controls_wb.electrical_path import ElectricalConnectionPath, RoutePoint, TerminalEndpoint, WireSegment
from controls_wb.gui.io_signal import _qt_widgets
from controls_wb.gui.project_intake import existing_project_object
from controls_wb.identity import CERoles, new_ce_identity
from controls_wb.model.electrical import materialize_electrical_device, materialize_electrical_path
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

    plc = _device_by_identity(project, values.get("plc_owner_identity", ""), CERoles.PLC_CONTROLLER)
    strip = _device_by_identity(project, values.get("terminal_strip_identity", ""), CERoles.TERMINAL_STRIP)
    device = _device_by_identity(project, values.get("device_owner_identity", ""), CERoles.FIELD_DEVICE)
    return _build_electrical_path(
        project,
        values,
        plc_identity=plc.CEIdentity,
        terminal_strip_identity=strip.CEIdentity,
        device_identity=device.CEIdentity,
    )


def add_electrical_path_from_form(document, values: dict[str, str]):
    project = existing_project_object(document) or create_or_update_project(document)
    normalized = dict(values)
    plc = _device_by_identity(project, normalized.get("plc_owner_identity", ""), CERoles.PLC_CONTROLLER)
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
        plc_identity=plc.CEIdentity,
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
    _add_device_items(plc_combo, _devices_for_role(project, CERoles.PLC_CONTROLLER))
    _add_device_items(strip_combo, _devices_for_role(project, CERoles.TERMINAL_STRIP))
    device_combo.addItem("Create new field device…", "")
    _add_device_items(device_combo, _devices_for_role(project, CERoles.FIELD_DEVICE))
    form.addRow("PLC", plc_combo)
    form.addRow("Terminal strip", strip_combo)
    form.addRow("Existing field device", device_combo)
    editors = {}
    for key, label, default in (
        ("device_tag", "New field-device tag", ""),
        ("device_description", "New device description", ""),
        ("signal_tag", "Signal tag", "DI-0001"),
        ("plc_terminal", "PLC channel terminal", "PLC1:X1.0"),
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
        plc_owner_identity=_combo_identity(plc_combo),
        terminal_strip_identity=_combo_identity(strip_combo),
        device_owner_identity=_combo_identity(device_combo),
    )
    result = add_electrical_path_from_form(document, values)
    if console is not None:
        console.PrintMessage(f"Electrical path added: {result.path_object.SignalTag}\n")
    return result

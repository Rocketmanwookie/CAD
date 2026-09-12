# SPDX-License-Identifier: MIT

import pytest

from controls_wb.gui.electrical_path import (
    add_electrical_path_from_form,
    build_electrical_path,
    parse_route_points,
)
from controls_wb.identity import CERoles
from controls_wb.model.electrical import materialize_electrical_device
from controls_wb.model.layout import create_starter_layout_objects
from controls_wb.model.project import create_or_update_project


class FakeObject:
    def __init__(self, name):
        self.Name = name
        self.PropertiesList = []

    def addProperty(self, property_type, name, group, description):
        self.PropertiesList.append(name)
        return self

    def setEditorMode(self, name, mode):
        pass


class FakeDocument:
    def __init__(self):
        self.Objects = []

    def addObject(self, object_type, name):
        obj = FakeObject(name)
        obj.ObjectType = object_type
        self.Objects.append(obj)
        return obj


def _setup():
    document = FakeDocument()
    project = create_or_update_project(document)
    layout = create_starter_layout_objects(document)
    device = materialize_electrical_device(document, "LS-001", description="Limit switch")
    values = {
        "plc_owner_identity": layout[4].CEIdentity,
        "terminal_strip_identity": layout[3].CEIdentity,
        "device_owner_identity": device.CEIdentity,
        "signal_tag": "DI-0001",
        "plc_terminal": "PLC1:X1.0",
        "terminal_in": "TB1:1-IN",
        "terminal_out": "TB1:1-OUT",
        "device_terminal": "LS-001:1",
        "conductor_size": "18 AWG",
        "color": "blue",
        "circuit_function": "dc_control",
        "wire_1_tag": "W-001",
        "wire_1_length_mm": "100",
        "wire_2_tag": "JMP-001",
        "wire_2_length_mm": "25",
        "wire_3_tag": "W-002",
        "wire_3_length_mm": "1000",
    }
    return document, project, values


def test_form_builds_required_plc_terminal_wire_terminal_wire_device_chain():
    _, project, values = _setup()

    path = build_electrical_path(project, values)

    assert [terminal.role for terminal in path.terminals] == [
        CERoles.PLC_CHANNEL_TERMINAL,
        CERoles.CABINET_TERMINAL,
        CERoles.CABINET_TERMINAL,
        CERoles.DEVICE_TERMINAL,
    ]
    assert [wire.wire_tag for wire in path.wires] == ["W-001", "JMP-001", "W-002"]
    assert path.total_length_mm == 1125.0


def test_form_service_materializes_and_registers_path():
    document, project, values = _setup()

    result = add_electrical_path_from_form(document, values)

    assert result.path_object in project.ElectricalPaths
    assert result.signal_object in project.ElectricalSignals
    assert result.path_object.SignalTag == "DI-0001"


def test_form_rejects_missing_required_size_and_nonpositive_length():
    _, project, values = _setup()
    values["conductor_size"] = ""
    with pytest.raises(ValueError, match="Conductor size"):
        build_electrical_path(project, values)

    values["conductor_size"] = "18 AWG"
    values["wire_3_length_mm"] = "0"
    with pytest.raises(ValueError, match="greater than zero"):
        build_electrical_path(project, values)


def test_new_device_is_identified_before_path_materialization():
    document, project, values = _setup()
    existing_device = next(
        device for device in project.ElectricalDevices
        if device.CERole == CERoles.FIELD_DEVICE
    )
    project.ElectricalDevices = [
        device for device in project.ElectricalDevices if device is not existing_device
    ]
    values["device_owner_identity"] = ""
    values["device_tag"] = "PE-002"

    result = add_electrical_path_from_form(document, values)

    owner_identity = result.terminal_objects[-1].OwnerIdentity
    created = next(device for device in project.ElectricalDevices if device.Tag == "PE-002")
    assert created.CERole == CERoles.FIELD_DEVICE
    assert created.CEIdentity == owner_identity


def test_invalid_form_does_not_create_requested_field_device():
    document, project, values = _setup()
    initial_objects = list(document.Objects)
    values.update(device_owner_identity="", device_tag="PE-003", wire_3_length_mm="0")

    with pytest.raises(ValueError, match="greater than zero"):
        add_electrical_path_from_form(document, values)

    assert document.Objects == initial_objects


def test_form_route_points_override_specified_length_in_schedule_graph():
    _, project, values = _setup()
    values["wire_1_route_mm"] = "0,0,0; 30,40,0; 30,40,100"
    values["wire_1_length_mm"] = "999"

    path = build_electrical_path(project, values)

    assert path.wires[0].specified_length_mm == 999.0
    assert path.wires[0].routed_length_mm == 150.0
    assert path.wires[0].effective_length_mm == 150.0
    assert path.total_length_mm == 1175.0


def test_route_can_supply_length_without_manual_fallback():
    _, project, values = _setup()
    values["wire_3_route_mm"] = "0,0,0;0,0,1000"
    values["wire_3_length_mm"] = ""

    path = build_electrical_path(project, values)

    assert path.wires[2].specified_length_mm is None
    assert path.wires[2].effective_length_mm == 1000.0


@pytest.mark.parametrize("route", ["0,0,0", "0,0;1,1,1", "0,0,0;nan,1,1"])
def test_route_parser_rejects_incomplete_or_nonfinite_routes(route):
    with pytest.raises(ValueError):
        parse_route_points(route, "Wire route")

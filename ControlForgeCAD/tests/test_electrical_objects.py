# SPDX-License-Identifier: MIT

from controls_wb.electrical_path import ElectricalConnectionPath, RoutePoint, TerminalEndpoint, WireSegment
from controls_wb.connections import connections_from_project
from controls_wb.identity import CERoles, new_ce_identity
from controls_wb.model.electrical import (
    electrical_path_from_object,
    materialize_electrical_device,
    materialize_electrical_path,
    update_electrical_path_object,
)
from dataclasses import replace
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
        obj.Document = self
        self.Objects.append(obj)
        return obj


def _path():
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, new_ce_identity(), "PLC1:X1.0")
    cabinet = TerminalEndpoint(new_ce_identity(), CERoles.CABINET_TERMINAL, new_ce_identity(), "TB1:1")
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, new_ce_identity(), "LS1:1")
    first = WireSegment(
        new_ce_identity(), plc.identity, cabinet.identity, "W-001",
        conductor_size="18 AWG", color="blue", circuit_function="dc_control",
        route=(RoutePoint(0, 0, 0), RoutePoint(0, 100, 0)),
        specified_length_mm=110,
    )
    second = WireSegment(
        new_ce_identity(), cabinet.identity, device.identity, "W-002",
        conductor_size="18 AWG", color="blue", circuit_function="dc_control",
        route=(RoutePoint(0, 100, 0), RoutePoint(0, 100, 250)),
    )
    return ElectricalConnectionPath(new_ce_identity(), new_ce_identity(), "DI-0001", (plc, cabinet, device), (first, second))


def test_materialized_path_creates_typed_identity_safe_linked_objects():
    document = FakeDocument()
    path = _path()

    result = materialize_electrical_path(document, path)

    assert len(document.Objects) == 7
    assert result.path_object.CEIdentity == path.identity
    assert result.signal_object.CEIdentity == path.signal_identity
    assert result.signal_object.CERole == CERoles.SIGNAL
    assert result.path_object.SignalObject is result.signal_object
    assert result.signal_object.ConnectionPaths == [result.path_object]
    assert result.path_object.CERole == CERoles.CONNECTION_PATH
    assert result.path_object.TerminalObjects == list(result.terminal_objects)
    assert result.path_object.WireObjects == list(result.wire_objects)
    assert [obj.CEIdentity for obj in result.terminal_objects] == [item.identity for item in path.terminals]
    assert [obj.CERole for obj in result.terminal_objects] == [item.role for item in path.terminals]
    assert result.wire_objects[0].FromTerminal is result.terminal_objects[0]
    assert result.wire_objects[0].ToTerminal is result.terminal_objects[1]
    assert result.wire_objects[0].CalculatedLength == "100.0 mm"
    assert result.wire_objects[0].HasSpecifiedLength is True
    assert result.wire_objects[0].SpecifiedLength == "110 mm"
    assert result.wire_objects[1].CalculatedLength == "250.0 mm"
    assert result.wire_objects[1].HasSpecifiedLength is False
    assert electrical_path_from_object(result.path_object) == path


def test_materialization_rejects_existing_identity_before_adding_objects():
    document = FakeDocument()
    path = _path()
    existing = document.addObject("App::FeaturePython", "Existing")
    existing.CEIdentity = path.terminals[0].identity

    try:
        materialize_electrical_path(document, path)
    except ValueError as exc:
        assert "already materialized" in str(exc)
    else:
        raise AssertionError("Expected duplicate identity rejection")

    assert document.Objects == [existing]


def test_materialized_signal_and_path_register_on_project_aggregate():
    document = FakeDocument()
    project = create_or_update_project(document)

    result = materialize_electrical_path(document, _path())

    assert project.ElectricalSignals == [result.signal_object]
    assert project.ElectricalPaths == [result.path_object]
    records = connections_from_project(project)
    assert len(records) == 1
    assert records[0].path_identity == result.path_object.CEIdentity
    assert records[0].terminal_identities == tuple(
        terminal.CEIdentity for terminal in result.terminal_objects
    )
    assert records[0].wire_identities == tuple(wire.CEIdentity for wire in result.wire_objects)


def test_materialized_device_receives_identity_role_and_project_registration_immediately():
    document = FakeDocument()
    project = create_or_update_project(document)

    device = materialize_electrical_device(
        document,
        "LS-001",
        manufacturer="Example",
        part_number="PROX-1",
        description="Proximity sensor",
    )

    assert device.CERole == CERoles.FIELD_DEVICE
    assert device.Tag == "LS-001"
    assert device in project.ElectricalDevices


def test_object_update_rejects_any_identity_change_before_mutation():
    document = FakeDocument()
    result = materialize_electrical_path(document, _path())
    current = electrical_path_from_object(result.path_object)
    changed = replace(current, identity=new_ce_identity(), signal_tag="SHOULD-NOT-APPLY")

    try:
        update_electrical_path_object(result.path_object, changed)
    except ValueError as exc:
        assert "cannot change" in str(exc)
    else:
        raise AssertionError("Expected immutable identity rejection")

    assert result.path_object.SignalTag == current.signal_tag


def test_object_update_rejects_duplicate_signal_tag_before_mutation():
    document = FakeDocument()
    result = materialize_electrical_path(document, _path())
    current = electrical_path_from_object(result.path_object)
    other_signal = document.addObject("App::FeaturePython", "OtherSignal")
    other_signal.CERole = CERoles.SIGNAL
    other_signal.SignalTag = "DI-EXISTING"
    other_signal.CEIdentity = new_ce_identity()

    try:
        update_electrical_path_object(
            result.path_object, replace(current, signal_tag="DI-EXISTING")
        )
    except ValueError as exc:
        assert "already uses tag" in str(exc)
    else:
        raise AssertionError("Expected duplicate signal-tag rejection")

    assert result.path_object.SignalTag == current.signal_tag
    assert result.signal_object.SignalTag == current.signal_tag

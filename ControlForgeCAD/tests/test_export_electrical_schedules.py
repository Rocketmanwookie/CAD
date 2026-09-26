# SPDX-License-Identifier: MIT

from controls_wb.commands.export_electrical_schedules import electrical_schedule_texts_for_objects
from controls_wb.electrical_path import ElectricalConnectionPath, TerminalEndpoint, WireSegment
from controls_wb.identity import CERoles, new_ce_identity
from controls_wb.model.electrical import materialize_electrical_path
from controls_wb.model.project import create_or_update_project
from controls_wb.model.layout import materialize_plc_allocation
import pytest


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


def test_electrical_schedule_command_helper_exports_project_typed_paths():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectId = "CE-SCHEDULE-001"
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1200"
    project.PlcCPU = "CPU 1212C DC/DC/DC"
    project.DICount = "1"
    channel = materialize_plc_allocation(document, project)["channels"][0]
    plc_owner = channel.CEIdentity
    device_owner = new_ce_identity()
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, plc_owner, channel.SignalAddress)
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, device_owner, "LS1:1")
    wire = WireSegment(
        new_ce_identity(), plc.identity, device.identity, "W-001",
        conductor_size="18 AWG", color="blue", specified_length_mm=1200,
    )
    path = ElectricalConnectionPath(new_ce_identity(), channel.AllocatedSignalObject.CEIdentity, "DI-0001", (plc, device), (wire,))
    materialize_electrical_path(document, path)

    wiring, io = electrical_schedule_texts_for_objects(document.Objects)

    assert "W-001" in wiring
    assert "18 AWG" in wiring
    assert "1200.0" in wiring
    assert "DI-0001" in io
    assert "%I0.0 > LS1:1" in io
    assert "PLCChannelIdentity" in wiring
    assert channel.CEIdentity in io
    assert "%I0.0" in io


def test_electrical_schedule_export_rejects_allocated_address_mismatch():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectId = "CE-SCHEDULE-002"
    project.PlcMake, project.PlcLine, project.PlcCPU, project.DICount = "Siemens", "S7-1200", "CPU 1212C DC/DC/DC", "1"
    channel = materialize_plc_allocation(document, project)["channels"][0]
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, channel.CEIdentity, "WRONG")
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, new_ce_identity(), "LS1:1")
    wire = WireSegment(new_ce_identity(), plc.identity, device.identity, "W-001", conductor_size="18 AWG", color="blue", specified_length_mm=1)
    materialize_electrical_path(document, ElectricalConnectionPath(new_ce_identity(), channel.AllocatedSignalObject.CEIdentity, "DI-0001", (plc, device), (wire,)))
    with pytest.raises(ValueError, match="address"):
        electrical_schedule_texts_for_objects(document.Objects)


def test_electrical_schedule_export_rejects_nonchannel_or_unregistered_owner():
    document = FakeDocument()
    project = create_or_update_project(document)
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, new_ce_identity(), "%I0.0")
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, new_ce_identity(), "LS1:1")
    wire = WireSegment(new_ce_identity(), plc.identity, device.identity, "W-001", conductor_size="18 AWG", color="blue", specified_length_mm=1)
    materialize_electrical_path(document, ElectricalConnectionPath(new_ce_identity(), new_ce_identity(), "DI-0001", (plc, device), (wire,)))
    with pytest.raises(ValueError, match="not an allocated"):
        electrical_schedule_texts_for_objects(document.Objects)


def test_electrical_schedule_export_rejects_channel_signal_mismatch():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectId, project.PlcMake, project.PlcLine, project.PlcCPU, project.DICount = "CE-SCHEDULE-003", "Siemens", "S7-1200", "CPU 1212C DC/DC/DC", "1"
    channel = materialize_plc_allocation(document, project)["channels"][0]
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, channel.CEIdentity, channel.SignalAddress)
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, new_ce_identity(), "LS1:1")
    wire = WireSegment(new_ce_identity(), plc.identity, device.identity, "W-001", conductor_size="18 AWG", color="blue", specified_length_mm=1)
    materialize_electrical_path(document, ElectricalConnectionPath(new_ce_identity(), channel.AllocatedSignalObject.CEIdentity, "DI-0001", (plc, device), (wire,)))
    channel.AllocatedSignalObject.CEIdentity = new_ce_identity()
    with pytest.raises(ValueError, match="signal"):
        electrical_schedule_texts_for_objects(document.Objects)

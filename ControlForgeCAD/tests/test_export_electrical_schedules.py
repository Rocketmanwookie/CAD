# SPDX-License-Identifier: MIT

from controls_wb.commands.export_electrical_schedules import electrical_schedule_texts_for_objects
from controls_wb.electrical_path import ElectricalConnectionPath, TerminalEndpoint, WireSegment
from controls_wb.identity import CERoles, new_ce_identity
from controls_wb.model.electrical import materialize_electrical_path
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


def test_electrical_schedule_command_helper_exports_project_typed_paths():
    document = FakeDocument()
    project = create_or_update_project(document)
    plc_owner = new_ce_identity()
    device_owner = new_ce_identity()
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, plc_owner, "PLC1:X1.0")
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, device_owner, "LS1:1")
    wire = WireSegment(
        new_ce_identity(), plc.identity, device.identity, "W-001",
        conductor_size="18 AWG", color="blue", specified_length_mm=1200,
    )
    path = ElectricalConnectionPath(new_ce_identity(), new_ce_identity(), "DI-0001", (plc, device), (wire,))
    materialize_electrical_path(document, path)

    wiring, io = electrical_schedule_texts_for_objects(document.Objects)

    assert "W-001" in wiring
    assert "18 AWG" in wiring
    assert "1200.0" in wiring
    assert "DI-0001" in io
    assert "PLC1:X1.0 > LS1:1" in io

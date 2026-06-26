# SPDX-License-Identifier: MIT

from controls_wb.commands.export_bom import collect_bom_rows
from controls_wb.model.layout import (
    STARTER_LAYOUT_SPECS,
    ControlsLayoutObject,
    create_starter_layout_objects,
    layout_object_metadata,
)


class FakeLayoutObject:
    def __init__(self, name):
        self.Name = name
        self.PropertiesList = []

    def addProperty(self, property_type, name, group, description):
        self.PropertiesList.append(name)
        return self


class FakeDocument:
    def __init__(self):
        self.Objects = []

    def addObject(self, object_type, name):
        obj = FakeLayoutObject(name)
        obj.ObjectType = object_type
        self.Objects.append(obj)
        return obj


def test_starter_layout_specs_cover_required_placeholder_types():
    names = {spec.name for spec in STARTER_LAYOUT_SPECS}

    assert {
        "CE_Backplate",
        "CE_DIN_Rail",
        "CE_Wire_Duct",
        "CE_Terminal_Strip",
        "CE_PLC_Rack",
    }.issubset(names)


def test_create_starter_layout_objects_adds_editable_properties():
    document = FakeDocument()

    objects = create_starter_layout_objects(document)

    assert [obj.Name for obj in objects] == [
        "CE_Backplate",
        "CE_DIN_Rail",
        "CE_Wire_Duct",
        "CE_Terminal_Strip",
        "CE_PLC_Rack",
    ]
    terminal_strip = objects[3]
    plc_rack = objects[4]
    assert isinstance(plc_rack.Proxy, ControlsLayoutObject)
    assert plc_rack.ObjectType == "Part::FeaturePython"
    assert "Tag" in plc_rack.PropertiesList
    assert "PanelName" in plc_rack.PropertiesList
    assert "TerminalCount" in plc_rack.PropertiesList
    assert "SlotNumber" in plc_rack.PropertiesList
    assert "ChannelCount" in plc_rack.PropertiesList
    assert terminal_strip.TerminalCount == 16
    assert plc_rack.Voltage == "24 VDC"
    assert plc_rack.ChannelCount == 16


def test_layout_object_metadata_is_pure_python():
    document = FakeDocument()
    plc_rack = create_starter_layout_objects(document)[4]

    assert layout_object_metadata(plc_rack) == {
        "Tag": "PLC-001",
        "Manufacturer": "",
        "PartNumber": "",
        "Description": "PLC rack/module placeholder",
        "PanelName": "PANEL-001",
        "Voltage": "24 VDC",
        "Current": "2 A",
        "TerminalCount": 0,
        "SlotNumber": 0,
        "ChannelCount": 16,
        "SignalType": "mixed_io",
    }


def test_layout_proxy_round_trips_persistent_state():
    document = FakeDocument()
    obj = create_starter_layout_objects(document)[0]

    state = obj.Proxy.__getstate__()
    restored = ControlsLayoutObject.__new__(ControlsLayoutObject)
    restored.__setstate__(state)

    assert restored.Type == "ControlsLayoutObject"


def test_bom_export_includes_starter_layout_objects_with_metadata():
    document = FakeDocument()
    objects = create_starter_layout_objects(document)
    objects[4].Manufacturer = "Generic"
    objects[4].PartNumber = "PLC-STARTER"

    rows = collect_bom_rows(objects)

    assert rows[0]["Tag"] == "PANEL-001"
    assert rows[0]["Description"] == "Control panel enclosure/backplate placeholder"
    assert rows[4] == {
        "Tag": "PLC-001",
        "Description": "PLC rack/module placeholder",
        "Manufacturer": "Generic",
        "PartNumber": "PLC-STARTER",
        "Quantity": 1,
    }

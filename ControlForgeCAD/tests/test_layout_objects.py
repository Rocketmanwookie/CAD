# SPDX-License-Identifier: MIT

from controls_wb.commands.export_bom import collect_bom_rows
from controls_wb.identity import CERoles, is_ce_identity
from controls_wb.model.layout import (
    STARTER_LAYOUT_SPECS,
    ControlsLayoutObject,
    create_starter_layout_objects,
    layout_object_metadata,
    allocation_electrical_graph_findings,
    materialize_plc_allocation,
    _prune_unlinked_allocation_occurrences,
    starter_layout_specs_for_project,
)
from controls_wb.model.project import create_or_update_project
import controls_wb.model.layout as layout_module


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


class StrictSlotLayoutObject(FakeLayoutObject):
    """Small FreeCAD-like fake that enforces integer slot properties."""

    def __init__(self, name):
        super().__init__(name)
        self._property_types = {}

    def addProperty(self, property_type, name, group, description):
        self._property_types[name] = property_type
        return super().addProperty(property_type, name, group, description)

    def __setattr__(self, name, value):
        property_types = self.__dict__.get("_property_types", {})
        if property_types.get(name) == "App::PropertyInteger" and not isinstance(value, int):
            raise TypeError(f"{name} must be int, not {type(value).__name__}")
        super().__setattr__(name, value)


class StrictSlotDocument(FakeDocument):
    def addObject(self, object_type, name):
        obj = StrictSlotLayoutObject(name)
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
    assert is_ce_identity(plc_rack.CEIdentity)
    assert plc_rack.CERole == CERoles.PLC_CONTROLLER
    assert terminal_strip.CERole == CERoles.TERMINAL_STRIP
    assert "PanelName" in plc_rack.PropertiesList
    assert "TerminalCount" in plc_rack.PropertiesList
    assert "SlotNumber" in plc_rack.PropertiesList
    assert "ChannelCount" in plc_rack.PropertiesList
    assert "CadModelPath" in plc_rack.PropertiesList
    assert "CadModelSha256" in plc_rack.PropertiesList
    assert terminal_strip.TerminalCount == 16
    assert objects[0].Manufacturer == "Generic"
    assert objects[0].PartNumber == "PANEL-BACKPLATE-800X1000"
    assert terminal_strip.PartNumber == "TERMINAL-STRIP-16"
    assert plc_rack.Voltage == "24 VDC"
    assert plc_rack.ChannelCount == 16


def test_layout_object_metadata_is_pure_python():
    document = FakeDocument()
    plc_rack = create_starter_layout_objects(document)[4]

    assert layout_object_metadata(plc_rack) == {
        "CEIdentity": plc_rack.CEIdentity,
        "CERole": CERoles.PLC_CONTROLLER,
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
        "CadModelPath": "",
        "CadModelFormat": "",
        "CadModelSha256": "",
    }


def test_starter_layout_specs_use_selected_plc_catalog_part():
    project = type(
        "Project",
        (),
        {
            "ProjectId": "CE-PROJECT-001",
            "PlcMake": "Siemens",
            "PlcLine": "S7-1200",
            "PlcCPU": "CPU 1214C DC/DC/DC",
        },
    )()

    plc_spec = starter_layout_specs_for_project(project)[4]

    assert plc_spec.manufacturer == "Siemens"
    assert plc_spec.part_number == "6ES7214-1AG40-0XB0"
    assert plc_spec.description == "CPU 1214C DC/DC/DC PLC CPU placeholder"
    assert plc_spec.channel_count == 26
    assert plc_spec.cad_model_format == "STEP"
    assert plc_spec.cad_model_path.endswith("Siemens S7-1200.STEP")


def test_create_starter_layout_objects_uses_existing_project_plc_selection():
    document = FakeDocument()
    project = type(
        "Project",
        (),
        {
            "ProjectId": "CE-PROJECT-001",
            "PlcMake": "Siemens",
            "PlcLine": "S7-1200",
            "PlcCPU": "CPU 1212C DC/DC/DC",
        },
    )()
    document.Objects.append(project)

    plc_rack = create_starter_layout_objects(document)[4]

    assert plc_rack.Manufacturer == "Siemens"
    assert plc_rack.PartNumber == "6ES7212-1AE40-0XB0"
    assert plc_rack.ChannelCount == 16
    assert plc_rack.CadModelFormat == "STEP"
    assert plc_rack.CadModelSha256 == "e5cdccde78115ef54856dfedc8705b5fc3031057e5db17068369b92e33a7e3b8"


def test_layout_proxy_round_trips_persistent_state():
    document = FakeDocument()
    obj = create_starter_layout_objects(document)[0]

    state = obj.Proxy.__getstate__()
    restored = ControlsLayoutObject.__new__(ControlsLayoutObject)
    restored.__setstate__(state)

    assert restored.Type == "ControlsLayoutObject"
    assert restored.Role == CERoles.PANEL


def test_allocation_occurrence_proxy_skips_zero_dimension_part_shape(monkeypatch):
    calls = []

    class FakePart:
        @staticmethod
        def makeBox(*dimensions):
            calls.append(dimensions)
            return object()

    monkeypatch.setattr(layout_module, "Part", FakePart)
    obj = FakeLayoutObject("CE_PLC_Channel")
    proxy = ControlsLayoutObject(obj, CERoles.PLC_CHANNEL)

    proxy.execute(obj)

    assert calls == []


def test_bom_export_includes_starter_layout_objects_with_metadata():
    document = FakeDocument()
    objects = create_starter_layout_objects(document)
    objects[4].Manufacturer = "Generic"
    objects[4].PartNumber = "PLC-STARTER"

    rows = collect_bom_rows(objects)

    assert rows[0]["Tag"] == "PANEL-001"
    assert rows[0] == {
        "Tag": "PANEL-001",
        "Description": "Generic 800 x 1000 mm enclosure/backplate placeholder",
        "Manufacturer": "Generic",
        "PartNumber": "PANEL-BACKPLATE-800X1000",
        "Quantity": 1,
    }
    assert rows[4] == {
        "Tag": "PLC-001",
        "Description": "PLC rack/module placeholder",
        "Manufacturer": "Generic",
        "PartNumber": "PLC-STARTER",
        "Quantity": 1,
    }


def test_starter_plc_and_terminal_strip_register_as_project_devices():
    document = FakeDocument()
    project = create_or_update_project(document)

    objects = create_starter_layout_objects(document)

    assert [obj.CERole for obj in project.ElectricalDevices] == [
        CERoles.TERMINAL_STRIP,
        CERoles.PLC_CONTROLLER,
    ]
    assert project.ElectricalDevices == [objects[3], objects[4]]


def test_materialized_plc_allocation_has_stable_rack_module_channel_links():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectId = "CE-ALLOC-001"
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1200"
    project.PlcCPU = "CPU 1212C DC/DC/DC"
    project.DICount = "9"

    first = materialize_plc_allocation(document, project)
    second = materialize_plc_allocation(document, project)

    assert first["rack"] is second["rack"]
    assert len(first["modules"]) == 2
    assert [(module.RackNumber, module.SlotNumber) for module in first["modules"]] == [("0", 1), ("0", 2)]
    assert len(first["channels"]) == 9
    assert first["modules"][0].Channels[0].AllocatedSignalTag == "DI-0001"
    assert first["modules"][1].Channels[0].AllocatedSignalTag == "DI-0009"
    assert first["modules"][1].Channels[0].ModuleObject is first["modules"][1]
    assert first["rack"].Modules == list(first["modules"])
    assert first["rack"].CERole == CERoles.PLC_RACK
    assert first["modules"][0].CERole == CERoles.PLC_MODULE
    assert first["channels"][0].CERole == CERoles.PLC_CHANNEL


def test_materialized_allocation_converts_persisted_string_slots_for_freecad_properties():
    document = StrictSlotDocument()
    project = create_or_update_project(document)
    project.ProjectId = "CE-ALLOC-STRING-SLOT-001"
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1200"
    project.PlcCPU = "CPU 1212C DC/DC/DC"
    project.DICount = "9"

    materialized = materialize_plc_allocation(document, project)

    assert [module.SlotNumber for module in materialized["modules"]] == [1, 2]
    assert {channel.SlotNumber for channel in materialized["channels"]} == {1, 2}


def test_materialized_plc_channels_link_to_deterministic_typed_signals():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectId = "CE-ALLOC-SIGNAL-001"
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1200"
    project.PlcCPU = "CPU 1212C DC/DC/DC"
    project.DICount = "1"

    first = materialize_plc_allocation(document, project)
    second = materialize_plc_allocation(document, project)
    channel = first["channels"][0]
    signal = channel.AllocatedSignalObject

    assert signal is second["channels"][0].AllocatedSignalObject
    assert signal.CERole == CERoles.SIGNAL
    assert signal.SignalTag == "DI-0001"
    assert signal.AllocatedChannelObject is channel
    assert signal in project.ElectricalSignals
    assert channel in project.ElectricalDevices


def test_allocation_graph_validation_reports_missing_reciprocal_and_unregistered_links():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectId = "CE-ALLOC-VALIDATE-001"
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1200"
    project.PlcCPU = "CPU 1212C DC/DC/DC"
    project.DICount = "1"
    channel = materialize_plc_allocation(document, project)["channels"][0]
    signal = channel.AllocatedSignalObject

    project.ElectricalSignals = []
    signal.AllocatedChannelObject = None
    findings = allocation_electrical_graph_findings(project, document.Objects)

    codes = {code for _, code, _ in findings}
    assert "allocated_channel_unregistered_signal" in codes
    assert "allocated_channel_reverse_link_missing" in codes


def test_pruning_unlinked_stale_channel_clears_and_retires_its_signal():
    document = FakeDocument()
    project = create_or_update_project(document)
    project.ProjectId = "CE-PRUNE-001"
    project.PlcMake = "Siemens"
    project.PlcLine = "S7-1200"
    project.PlcCPU = "CPU 1212C DC/DC/DC"
    project.DICount = "1"
    channel = materialize_plc_allocation(document, project)["channels"][0]
    signal = channel.AllocatedSignalObject

    _prune_unlinked_allocation_occurrences(document, project, set())

    assert channel not in document.Objects
    assert signal not in project.ElectricalSignals
    assert signal.AllocatedChannelObject is None

# SPDX-License-Identifier: MIT
"""Starter controls layout objects for FreeCAD documents."""

from __future__ import annotations

from dataclasses import dataclass

try:
    import FreeCAD as App
    import Part
except Exception:  # pragma: no cover
    App = None
    Part = None


@dataclass(frozen=True)
class LayoutObjectSpec:
    name: str
    tag: str
    description: str
    panel_name: str
    width: str
    height: str
    depth: str
    manufacturer: str = ""
    part_number: str = ""
    voltage: str = ""
    current: str = ""
    terminal_count: int = 0
    slot_number: int = 0
    channel_count: int = 0
    signal_type: str = ""


STARTER_LAYOUT_SPECS = (
    LayoutObjectSpec(
        name="CE_Backplate",
        tag="PANEL-001",
        description="Control panel enclosure/backplate placeholder",
        panel_name="PANEL-001",
        width="800 mm",
        height="1000 mm",
        depth="3 mm",
    ),
    LayoutObjectSpec(
        name="CE_DIN_Rail",
        tag="DIN-001",
        description="DIN rail placeholder",
        panel_name="PANEL-001",
        width="600 mm",
        height="35 mm",
        depth="7.5 mm",
    ),
    LayoutObjectSpec(
        name="CE_Wire_Duct",
        tag="DUCT-001",
        description="Wire duct placeholder",
        panel_name="PANEL-001",
        width="600 mm",
        height="80 mm",
        depth="60 mm",
    ),
    LayoutObjectSpec(
        name="CE_Terminal_Strip",
        tag="TB-001",
        description="Terminal strip placeholder",
        panel_name="PANEL-001",
        width="300 mm",
        height="45 mm",
        depth="50 mm",
        terminal_count=16,
    ),
    LayoutObjectSpec(
        name="CE_PLC_Rack",
        tag="PLC-001",
        description="PLC rack/module placeholder",
        panel_name="PANEL-001",
        width="250 mm",
        height="120 mm",
        depth="90 mm",
        voltage="24 VDC",
        current="2 A",
        slot_number=0,
        channel_count=16,
        signal_type="mixed_io",
    ),
)


LAYOUT_PROPERTY_SPECS = (
    ("App::PropertyString", "Tag", "Controls", "Device tag"),
    ("App::PropertyString", "Manufacturer", "Controls", "Manufacturer"),
    ("App::PropertyString", "PartNumber", "Controls", "Part number"),
    ("App::PropertyString", "Description", "Controls", "Description"),
    ("App::PropertyString", "PanelName", "Controls", "Panel name"),
    ("App::PropertyString", "Voltage", "Electrical", "Nominal voltage"),
    ("App::PropertyString", "Current", "Electrical", "Nominal current"),
    ("App::PropertyInteger", "TerminalCount", "Controls", "Terminal count"),
    ("App::PropertyInteger", "SlotNumber", "Controls", "PLC slot number"),
    ("App::PropertyInteger", "ChannelCount", "Controls", "I/O channel count"),
    ("App::PropertyString", "SignalType", "Controls", "Signal type"),
    ("App::PropertyLength", "Width", "Geometry", "Placeholder width"),
    ("App::PropertyLength", "Height", "Geometry", "Placeholder height"),
    ("App::PropertyLength", "Depth", "Geometry", "Placeholder depth"),
)


def ensure_layout_properties(obj) -> None:
    existing = set(getattr(obj, "PropertiesList", []) or [])
    for property_type, name, group, description in LAYOUT_PROPERTY_SPECS:
        if name not in existing:
            obj.addProperty(property_type, name, group, description)


def apply_layout_spec(obj, spec: LayoutObjectSpec):
    obj.Tag = spec.tag
    obj.Manufacturer = spec.manufacturer
    obj.PartNumber = spec.part_number
    obj.Description = spec.description
    obj.PanelName = spec.panel_name
    obj.Voltage = spec.voltage
    obj.Current = spec.current
    obj.TerminalCount = spec.terminal_count
    obj.SlotNumber = spec.slot_number
    obj.ChannelCount = spec.channel_count
    obj.SignalType = spec.signal_type
    obj.Width = spec.width
    obj.Height = spec.height
    obj.Depth = spec.depth
    return obj


def layout_object_metadata(obj) -> dict[str, object]:
    return {
        "Tag": getattr(obj, "Tag", ""),
        "Manufacturer": getattr(obj, "Manufacturer", ""),
        "PartNumber": getattr(obj, "PartNumber", ""),
        "Description": getattr(obj, "Description", ""),
        "PanelName": getattr(obj, "PanelName", ""),
        "Voltage": getattr(obj, "Voltage", ""),
        "Current": getattr(obj, "Current", ""),
        "TerminalCount": getattr(obj, "TerminalCount", 0),
        "SlotNumber": getattr(obj, "SlotNumber", 0),
        "ChannelCount": getattr(obj, "ChannelCount", 0),
        "SignalType": getattr(obj, "SignalType", ""),
    }


def create_layout_object(document, spec: LayoutObjectSpec):
    obj = document.addObject("Part::FeaturePython", spec.name)
    ControlsLayoutObject(obj)
    return apply_layout_spec(obj, spec)


def create_starter_layout_objects(document=None) -> list[object]:
    if document is None:
        document = App.ActiveDocument
    return [create_layout_object(document, spec) for spec in STARTER_LAYOUT_SPECS]


class ControlsLayoutObject:
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "ControlsLayoutObject"
        ensure_layout_properties(obj)

    def execute(self, obj):
        if Part is not None:
            obj.Shape = Part.makeBox(obj.Width, obj.Depth, obj.Height)

    def __getstate__(self):
        return {"Type": self.Type}

    def __setstate__(self, state):
        self.Type = state.get("Type", "ControlsLayoutObject")

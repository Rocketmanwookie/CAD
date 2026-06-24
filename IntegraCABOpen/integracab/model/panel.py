# SPDX-License-Identifier: MIT
"""Parametric panel/backplate placeholder model."""

try:
    import FreeCAD as App
    import Part
except Exception:  # pragma: no cover
    App = None
    Part = None


def create_panel(name: str, width="800 mm", height="1000 mm", depth="3 mm"):
    """Create a simple FreeCAD FeaturePython backplate object."""
    obj = App.ActiveDocument.addObject("Part::FeaturePython", name)
    ControlPanel(obj)
    obj.Width = width
    obj.Height = height
    obj.Depth = depth
    obj.Tag = "PANEL-001"
    obj.Manufacturer = ""
    obj.PartNumber = ""
    obj.Description = "Control panel backplate"
    return obj


class ControlPanel:
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "ControlPanel"
        obj.addProperty("App::PropertyString", "Tag", "Controls", "Device tag")
        obj.addProperty("App::PropertyString", "Manufacturer", "Controls", "Manufacturer")
        obj.addProperty("App::PropertyString", "PartNumber", "Controls", "Part number")
        obj.addProperty("App::PropertyString", "Description", "Controls", "Description")
        obj.addProperty("App::PropertyLength", "Width", "Geometry", "Panel width")
        obj.addProperty("App::PropertyLength", "Height", "Geometry", "Panel height")
        obj.addProperty("App::PropertyLength", "Depth", "Geometry", "Panel thickness")

    def execute(self, obj):
        if Part is not None:
            obj.Shape = Part.makeBox(obj.Width, obj.Depth, obj.Height)

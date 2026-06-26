# SPDX-License-Identifier: MIT
"""FreeCAD project/intake object wrapper."""

try:
    import FreeCAD as App
except Exception:  # pragma: no cover
    App = None

from controls_wb.intake import SCHEMA_VERSION, default_project_intake


def create_project(name: str = "Controls Project"):
    """Create a lightweight CEProject object in the active FreeCAD document."""
    obj = App.ActiveDocument.addObject("App::FeaturePython", "CE_Project")
    ControlsProject(obj)
    intake = default_project_intake(name=name)
    obj.ProjectId = intake.project_id
    obj.ProjectName = intake.name
    obj.SchemaVersion = intake.schema_version
    obj.Deliverables = sorted(intake.deliverables)
    obj.PowerFeedStatus = "Requested"
    obj.PlcPlatformStatus = "Requested"
    obj.SensorCountStatus = "Requested"
    return obj


class ControlsProject:
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "ControlsProject"
        obj.addProperty("App::PropertyString", "ProjectId", "CEProject", "CEProject identifier")
        obj.addProperty("App::PropertyString", "ProjectName", "CEProject", "Project name")
        obj.addProperty("App::PropertyString", "SchemaVersion", "CEProject", "CEProject schema version")
        obj.addProperty("App::PropertyStringList", "Deliverables", "Intake", "Selected deliverables")
        obj.addProperty("App::PropertyString", "PowerFeedStatus", "Intake", "Power feed intake status")
        obj.addProperty("App::PropertyString", "PlcPlatformStatus", "Intake", "PLC platform intake status")
        obj.addProperty("App::PropertyString", "SensorCountStatus", "Intake", "Sensor count intake status")

    def execute(self, obj):
        return None

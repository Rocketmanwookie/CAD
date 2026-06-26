# SPDX-License-Identifier: MIT
"""Create an initial controls-engineering project object."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.model.project import create_or_update_project


class NewProjectCommand:
    def GetResources(self):
        return {
            "MenuText": "New Controls Project",
            "ToolTip": "Create an initial CEProject intake object.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        create_or_update_project(App.ActiveDocument)
        App.ActiveDocument.recompute()

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_NewProject", NewProjectCommand())

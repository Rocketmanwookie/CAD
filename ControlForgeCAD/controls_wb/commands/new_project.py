# SPDX-License-Identifier: MIT
"""Create an initial controls-engineering project object."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.gui.project_intake import show_project_intake_dialog
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
        try:
            parent = Gui.getMainWindow() if Gui is not None and hasattr(Gui, "getMainWindow") else None
            project = show_project_intake_dialog(App.ActiveDocument, parent=parent, console=App.Console)
        except RuntimeError as exc:
            project = create_or_update_project(App.ActiveDocument)
            App.Console.PrintWarning(f"{exc} Created starter CE_Project without dialog.\n")
        if project is not None:
            App.Console.PrintMessage(f"Controls project ready: {project.ProjectName}\n")
        App.ActiveDocument.recompute()

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_NewProject", NewProjectCommand())

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
from controls_wb.project_workspace import bind_project_workspace, load_workspace_parent, save_workspace_parent
from controls_wb.freecad_transactions import document_transaction


class NewProjectCommand:
    def GetResources(self):
        return {
            "MenuText": "New Controls Project",
            "ToolTip": "Create an initial CEProject intake object.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        with document_transaction(App.ActiveDocument, "Create controls project"):
            try:
                parent = Gui.getMainWindow() if Gui is not None and hasattr(Gui, "getMainWindow") else None
                project = show_project_intake_dialog(App.ActiveDocument, parent=parent, console=App.Console)
            except RuntimeError as exc:
                project = create_or_update_project(App.ActiveDocument)
                App.Console.PrintWarning(f"{exc} Created starter CE_Project without dialog.\n")
            if project is not None and not str(getattr(project, "ProjectRoot", "") or "").strip():
                workspace = _select_and_bind_workspace(project, parent)
                if workspace is not None:
                    save_as = getattr(App.ActiveDocument, "saveAs", None)
                    if callable(save_as) and not workspace.fcstd_path.exists():
                        save_as(str(workspace.fcstd_path))
            App.ActiveDocument.recompute()
        if project is not None:
            App.Console.PrintMessage(f"Controls project ready: {project.ProjectName}\n")

    def IsActive(self):
        return App is not None


def _select_and_bind_workspace(project, parent=None):
    """Ask once for the workspace parent after a project name is confirmed."""

    if Gui is None:
        return None
    try:
        from PySide import QtGui
    except Exception:  # pragma: no cover - FreeCAD may expose PySide2 instead.
        try:
            from PySide2 import QtWidgets as QtGui
        except Exception:
            return None
    from pathlib import Path

    suggested_parent = load_workspace_parent(App, Path.home() / "Documents")
    selected_parent = QtGui.QFileDialog.getExistingDirectory(
        parent,
        "Choose the parent folder for this ControlForgeCAD project",
        str(suggested_parent),
    )
    if not selected_parent:
        return None
    selected_path = Path(selected_parent)
    save_workspace_parent(App, selected_path)
    return bind_project_workspace(project, selected_path)


if Gui is not None:
    Gui.addCommand("CE_NewProject", NewProjectCommand())

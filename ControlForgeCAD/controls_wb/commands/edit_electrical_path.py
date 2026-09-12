# SPDX-License-Identifier: MIT
"""Edit a selected typed electrical path without changing graph identities."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.freecad_transactions import document_transaction
from controls_wb.gui.electrical_path import show_edit_electrical_path_dialog
from controls_wb.identity import CERoles


def selected_electrical_path(selection):
    paths = [obj for obj in selection if getattr(obj, "CERole", "") == CERoles.CONNECTION_PATH]
    if len(paths) != 1:
        raise ValueError("Select exactly one typed electrical path to edit.")
    return paths[0]


class EditElectricalPathCommand:
    def GetResources(self):
        return {
            "MenuText": "Edit Electrical Path",
            "ToolTip": "Edit terminal, wire, and route data while preserving CE identities.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        try:
            path_obj = selected_electrical_path(Gui.Selection.getSelection())
            parent = Gui.getMainWindow() if hasattr(Gui, "getMainWindow") else None
            with document_transaction(App.ActiveDocument, "Edit electrical path"):
                show_edit_electrical_path_dialog(path_obj, parent=parent, console=App.Console)
                App.ActiveDocument.recompute()
        except (RuntimeError, ValueError) as exc:
            App.Console.PrintWarning(f"{exc} Electrical path was not changed.\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_EditElectricalPath", EditElectricalPathCommand())

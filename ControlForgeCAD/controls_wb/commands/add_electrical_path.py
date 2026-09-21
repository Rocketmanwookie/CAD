# SPDX-License-Identifier: MIT
"""Create a typed continuous PLC-to-device electrical path."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.freecad_transactions import document_transaction
from controls_wb.gui.electrical_path import show_electrical_path_dialog


class AddElectricalPathCommand:
    def GetResources(self):
        return {
            "MenuText": "Add Electrical Path",
            "ToolTip": "Create a continuous PLC-terminal-to-device-terminal wiring path.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        try:
            parent = Gui.getMainWindow() if Gui is not None and hasattr(Gui, "getMainWindow") else None
            with document_transaction(App.ActiveDocument, "Add electrical path"):
                show_electrical_path_dialog(App.ActiveDocument, parent=parent, console=App.Console)
                App.ActiveDocument.recompute()
        except (RuntimeError, ValueError) as exc:
            App.Console.PrintWarning(f"{exc} Electrical path was not added.\n")

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_AddElectricalPath", AddElectricalPathCommand())

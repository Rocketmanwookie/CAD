# SPDX-License-Identifier: MIT
"""Add a traceable signal-to-terminal-to-wire connection record."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.gui.connection import show_connection_dialog
from controls_wb.freecad_transactions import document_transaction


class AddConnectionCommand:
    def GetResources(self):
        return {"MenuText": "Add Connection Record", "ToolTip": "Add a traceable signal-to-terminal-to-wire record."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        try:
            parent = Gui.getMainWindow() if Gui is not None and hasattr(Gui, "getMainWindow") else None
            with document_transaction(App.ActiveDocument, "Add connection record"):
                show_connection_dialog(App.ActiveDocument, parent=parent, console=App.Console)
                App.ActiveDocument.recompute()
        except (RuntimeError, ValueError) as exc:
            App.Console.PrintWarning(f"{exc} Connection record was not added.\n")
            return

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_AddConnection", AddConnectionCommand())

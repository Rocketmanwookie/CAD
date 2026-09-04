# SPDX-License-Identifier: MIT
"""Add a traceable signal-to-terminal-to-wire connection record."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.gui.connection import show_connection_dialog


class AddConnectionCommand:
    def GetResources(self):
        return {"MenuText": "Add Connection Record", "ToolTip": "Add a traceable signal-to-terminal-to-wire record."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        try:
            parent = Gui.getMainWindow() if Gui is not None and hasattr(Gui, "getMainWindow") else None
            show_connection_dialog(App.ActiveDocument, parent=parent, console=App.Console)
        except (RuntimeError, ValueError) as exc:
            App.Console.PrintWarning(f"{exc} Connection record was not added.\n")
            return
        App.ActiveDocument.recompute()

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_AddConnection", AddConnectionCommand())

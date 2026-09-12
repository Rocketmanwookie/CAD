# SPDX-License-Identifier: MIT
"""Add a labeled I/O signal to the active controls project."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.gui.io_signal import show_io_signal_dialog
from controls_wb.freecad_transactions import document_transaction


class AddIOSignalCommand:
    def GetResources(self):
        return {
            "MenuText": "Add I/O Signal",
            "ToolTip": "Add a labeled I/O signal with an auto-generated tag and address.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        try:
            parent = Gui.getMainWindow() if Gui is not None and hasattr(Gui, "getMainWindow") else None
            with document_transaction(App.ActiveDocument, "Add I/O signal"):
                show_io_signal_dialog(App.ActiveDocument, parent=parent, console=App.Console)
                App.ActiveDocument.recompute()
        except RuntimeError as exc:
            App.Console.PrintWarning(f"{exc} I/O signal was not added.\n")
            return

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_AddIOSignal", AddIOSignalCommand())

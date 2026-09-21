# SPDX-License-Identifier: MIT
"""Create a parametric control panel placeholder."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.model.layout import create_starter_layout_objects
from controls_wb.freecad_transactions import document_transaction


class CreatePanelCommand:
    def GetResources(self):
        return {
            "MenuText": "Create Control Panel",
            "ToolTip": "Create starter controls layout placeholders.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsPanel")
        with document_transaction(App.ActiveDocument, "Create control panel"):
            created = create_starter_layout_objects(App.ActiveDocument)
            App.ActiveDocument.recompute()
        App.Console.PrintMessage(f"Created {len(created)} starter controls layout objects.\n")

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_CreatePanel", CreatePanelCommand())

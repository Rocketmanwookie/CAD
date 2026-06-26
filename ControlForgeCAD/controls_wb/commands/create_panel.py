# SPDX-License-Identifier: MIT
"""Create a parametric control panel placeholder."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.model.layout import create_starter_layout_objects


class CreatePanelCommand:
    def GetResources(self):
        return {
            "MenuText": "Create Control Panel",
            "ToolTip": "Create starter controls layout placeholders.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsPanel")
        created = create_starter_layout_objects(App.ActiveDocument)
        App.Console.PrintMessage(f"Created {len(created)} starter controls layout objects.\n")
        App.ActiveDocument.recompute()

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_CreatePanel", CreatePanelCommand())

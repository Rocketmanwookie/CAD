# SPDX-License-Identifier: MIT
"""Create a parametric control panel placeholder."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from integracab.model.panel import create_panel


class CreatePanelCommand:
    def GetResources(self):
        return {"MenuText": "Create Control Panel", "ToolTip": "Create a parametric electrical control panel backplate."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("IntegraCABPanel")
        create_panel(name="ICAB_Backplate", width="800 mm", height="1000 mm", depth="3 mm")
        App.ActiveDocument.recompute()

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("ICAB_CreatePanel", CreatePanelCommand())

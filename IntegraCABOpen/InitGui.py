# SPDX-License-Identifier: MIT
"""FreeCAD GUI workbench registration for IntegraCAB Open."""

import os

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover - executed only outside FreeCAD
    App = None
    Gui = None


if Gui is not None:

    class IntegraCABOpenWorkbench(Workbench):  # type: ignore[name-defined]
        MenuText = "Controls / Automation"
        ToolTip = "IntegraCAB Open: controls-engineering intake, validation, PLC I/O, CAD integration, and XML interchange."

        def Initialize(self):
            base_dir = os.path.dirname(__file__)
            Gui.addIconPath(os.path.join(base_dir, "integracab", "resources", "icons"))

            from integracab.commands import create_panel, export_bom_source, validate_project  # noqa: F401

            self.layout_commands = ["ICAB_CreatePanel"]
            self.integration_commands = ["ICAB_ExportBOMSource", "ICAB_ValidateProject"]

            self.appendToolbar("Controls Layout", self.layout_commands)
            self.appendToolbar("Controls Integration", self.integration_commands)
            self.appendMenu("Controls / Automation", self.layout_commands)
            self.appendMenu(["Controls / Automation", "Integration"], self.integration_commands)

        def Activated(self):
            if App:
                App.Console.PrintMessage("IntegraCAB Open workbench activated\n")

        def Deactivated(self):
            if App:
                App.Console.PrintMessage("IntegraCAB Open workbench deactivated\n")

        def ContextMenu(self, recipient):
            self.appendContextMenu("Controls / Automation", self.layout_commands)

        def GetClassName(self):
            return "Gui::PythonWorkbench"


    Gui.addWorkbench(IntegraCABOpenWorkbench())

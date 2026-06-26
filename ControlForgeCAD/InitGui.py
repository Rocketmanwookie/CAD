# SPDX-License-Identifier: MIT
"""FreeCAD GUI workbench registration for ControlForgeCAD."""

import os

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover - executed only outside FreeCAD
    App = None
    Gui = None


if Gui is not None:

    class ControlsEngineeringWorkbench(Workbench):  # type: ignore[name-defined]
        MenuText = "Controls / Automation"
        ToolTip = "Controls engineering tools for PLC I/O, panel layouts, wiring, BOMs, safety circuits, and XML interchange."

        def Initialize(self):
            base_dir = os.path.dirname(__file__)
            Gui.addIconPath(os.path.join(base_dir, "controls_wb", "resources", "icons"))

            from controls_wb.commands import create_panel, export_bom, new_project, validate_project  # noqa: F401

            self.project_commands = ["CE_NewProject"]
            self.layout_commands = ["CE_CreatePanel"]
            self.export_commands = ["CE_ExportBOM", "CE_ValidateProject"]

            self.appendToolbar("Controls Project", self.project_commands)
            self.appendToolbar("Controls Layout", self.layout_commands)
            self.appendToolbar("Controls Exports", self.export_commands)
            self.appendMenu("Controls / Automation", self.project_commands + self.layout_commands)
            self.appendMenu(["Controls / Automation", "Exports"], self.export_commands)

        def Activated(self):
            if App:
                App.Console.PrintMessage("Controls Engineering Workbench activated\n")

        def Deactivated(self):
            if App:
                App.Console.PrintMessage("Controls Engineering Workbench deactivated\n")

        def ContextMenu(self, recipient):
            self.appendContextMenu("Controls / Automation", self.project_commands + self.layout_commands)

        def GetClassName(self):
            return "Gui::PythonWorkbench"


    Gui.addWorkbench(ControlsEngineeringWorkbench())

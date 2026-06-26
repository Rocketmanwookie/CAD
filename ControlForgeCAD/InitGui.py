# SPDX-License-Identifier: MIT
"""FreeCAD GUI workbench registration for ControlForgeCAD."""

import os

from controls_wb.commands.metadata import (
    EXPORT_COMMANDS,
    LAYOUT_COMMANDS,
    PROJECT_COMMANDS,
    VALIDATION_COMMANDS,
)

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

            from controls_wb.commands import (  # noqa: F401
                create_panel,
                export_bom,
                export_ceproject_xml,
                missing_data,
                new_project,
                validate_project,
            )

            self.project_commands = list(PROJECT_COMMANDS)
            self.layout_commands = list(LAYOUT_COMMANDS)
            self.validation_commands = list(VALIDATION_COMMANDS)
            self.export_commands = list(EXPORT_COMMANDS)

            self.appendToolbar("Controls Project", self.project_commands)
            self.appendToolbar("Controls Layout", self.layout_commands)
            self.appendToolbar("Controls Validation", self.validation_commands)
            self.appendToolbar("Controls Exports", self.export_commands)
            self.appendMenu(
                "Controls / Automation",
                self.project_commands + self.layout_commands + self.validation_commands,
            )
            self.appendMenu(["Controls / Automation", "Exports"], self.export_commands)

        def Activated(self):
            if App:
                App.Console.PrintMessage("Controls Engineering Workbench activated\n")

        def Deactivated(self):
            if App:
                App.Console.PrintMessage("Controls Engineering Workbench deactivated\n")

        def ContextMenu(self, recipient):
            self.appendContextMenu(
                "Controls / Automation",
                self.project_commands + self.layout_commands + self.validation_commands,
            )

        def GetClassName(self):
            return "Gui::PythonWorkbench"


    Gui.addWorkbench(ControlsEngineeringWorkbench())

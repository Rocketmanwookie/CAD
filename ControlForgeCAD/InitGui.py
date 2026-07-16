# SPDX-License-Identifier: MIT
"""FreeCAD GUI workbench registration for ControlForgeCAD.

This file intentionally keeps imports used by workbench methods inside those
methods. Some FreeCAD loaders execute InitGui.py with separate globals and
locals dictionaries; in that mode, names imported or defined at module scope may
not be visible from methods later called by FreeCAD. Keeping method dependencies
local makes the workbench load path robust in that environment.
"""

try:
    import FreeCADGui as Gui
except Exception:  # pragma: no cover - executed only outside FreeCAD
    Gui = None


if Gui is not None:

    class ControlsEngineeringWorkbench(Workbench):  # type: ignore[name-defined]
        MenuText = "Controls / Automation"
        ToolTip = (
            "Controls engineering tools for PLC I/O, panel layouts, wiring, "
            "BOMs, safety circuits, and XML interchange."
        )

        def _workbench_root(self):
            """Return the ControlForgeCAD workbench root without relying on module globals."""

            import os
            import sys
            from pathlib import Path

            module_file = globals().get("__file__")
            if module_file:
                return str(Path(module_file).resolve().parent)

            module_spec = globals().get("__spec__")
            spec_origin = getattr(module_spec, "origin", None)
            if spec_origin and spec_origin not in {"built-in", "frozen", "namespace"}:
                return str(Path(spec_origin).resolve().parent)

            try:
                import controls_wb

                package_file = getattr(controls_wb, "__file__", None)
                if package_file:
                    return str(Path(package_file).resolve().parent.parent)

                package_paths = getattr(controls_wb, "__path__", None)
                if package_paths:
                    for package_path in package_paths:
                        return str(Path(package_path).resolve().parent)
            except Exception:
                pass

            for raw_entry in sys.path:
                if not raw_entry:
                    continue

                entry = Path(raw_entry).expanduser()

                if (entry / "InitGui.py").is_file() and (entry / "controls_wb").is_dir():
                    return str(entry.resolve())

                if entry.name == "ControlForgeCAD" and (entry / "controls_wb").is_dir():
                    return str(entry.resolve())

                candidate = entry / "ControlForgeCAD"
                if (candidate / "InitGui.py").is_file() and (candidate / "controls_wb").is_dir():
                    return str(candidate.resolve())

            return os.getcwd()

        def Initialize(self):
            import os
            import FreeCADGui as Gui

            from controls_wb.commands.metadata import (
                EXPORT_COMMANDS,
                LAYOUT_COMMANDS,
                PROJECT_COMMANDS,
                VALIDATION_COMMANDS,
            )

            base_dir = self._workbench_root()
            Gui.addIconPath(os.path.join(base_dir, "controls_wb", "resources", "icons"))

            from controls_wb.commands import (  # noqa: F401
                create_panel,
                export_bom,
                export_ceproject_xml,
                export_io_list,
                export_missing_data_csv,
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
            try:
                import FreeCAD as App

                App.Console.PrintMessage("Controls Engineering Workbench activated\n")
            except Exception:
                pass

        def Deactivated(self):
            try:
                import FreeCAD as App

                App.Console.PrintMessage("Controls Engineering Workbench deactivated\n")
            except Exception:
                pass

        def ContextMenu(self, recipient):
            self.appendContextMenu(
                "Controls / Automation",
                self.project_commands + self.layout_commands + self.validation_commands,
            )

        def GetClassName(self):
            return "Gui::PythonWorkbench"


    Gui.addWorkbench(ControlsEngineeringWorkbench())

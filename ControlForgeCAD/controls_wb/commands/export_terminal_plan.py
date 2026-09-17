# SPDX-License-Identifier: MIT
"""Export a validated terminal plan from typed electrical paths."""

from pathlib import Path

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.electrical_validation import validate_connection_graph
from controls_wb.model.electrical import electrical_paths_from_project
from controls_wb.terminal_plan import terminal_plan_csv


def terminal_plan_text_for_objects(objects) -> str:
    paths = []
    owners, signals = set(), set()
    for project in objects:
        if not hasattr(project, "ElectricalPaths"):
            continue
        paths.extend(electrical_paths_from_project(project))
        owners.update(getattr(device, "CEIdentity", "") for device in getattr(project, "ElectricalDevices", []) or [])
        signals.update(getattr(signal, "CEIdentity", "") for signal in getattr(project, "ElectricalSignals", []) or [])
    findings = validate_connection_graph(tuple(paths), known_owner_identities=owners, known_signal_identities=signals)
    errors = [finding.message for finding in findings if finding.severity == "ERROR"]
    if errors:
        raise ValueError("Terminal plan preflight failed: " + "; ".join(errors))
    return terminal_plan_csv(tuple(paths))


class ExportTerminalPlanCommand:
    def GetResources(self):
        return {"MenuText": "Export Terminal Plan", "ToolTip": "Export validated cabinet-terminal connections to CSV."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        try:
            text = terminal_plan_text_for_objects(App.ActiveDocument.Objects)
        except ValueError as exc:
            App.Console.PrintError(f"Terminal plan was not exported: {exc}\n")
            return
        target = Path.home() / "integracad_terminal_plan.csv"
        target.write_text(text, encoding="utf-8")
        App.Console.PrintMessage(f"Terminal plan exported to {target}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportTerminalPlan", ExportTerminalPlanCommand())

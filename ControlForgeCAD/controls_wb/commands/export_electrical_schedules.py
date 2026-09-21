# SPDX-License-Identifier: MIT
"""Export canonical typed wiring and I/O path schedules."""

from pathlib import Path

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.electrical_path import io_path_schedule_csv, wiring_schedule_csv
from controls_wb.model.electrical import electrical_paths_from_project


def electrical_schedule_texts_for_objects(objects) -> tuple[str, str]:
    paths = []
    for obj in objects:
        if hasattr(obj, "ElectricalPaths"):
            paths.extend(electrical_paths_from_project(obj))
    typed_paths = tuple(paths)
    return wiring_schedule_csv(typed_paths), io_path_schedule_csv(typed_paths)


class ExportElectricalSchedulesCommand:
    def GetResources(self):
        return {
            "MenuText": "Export Electrical Schedules",
            "ToolTip": "Export identity-safe wiring and I/O path schedules from typed electrical paths.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        try:
            wiring_text, io_text = electrical_schedule_texts_for_objects(App.ActiveDocument.Objects)
        except ValueError as exc:
            App.Console.PrintError(f"Electrical schedules were not exported: {exc}\n")
            return
        wiring_path = Path.home() / "integracad_wiring_schedule.csv"
        io_path = Path.home() / "integracad_io_path_schedule.csv"
        wiring_path.write_text(wiring_text, encoding="utf-8")
        io_path.write_text(io_text, encoding="utf-8")
        App.Console.PrintMessage(f"Wiring schedule exported to {wiring_path}\n")
        App.Console.PrintMessage(f"I/O path schedule exported to {io_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportElectricalSchedules", ExportElectricalSchedulesCommand())

# SPDX-License-Identifier: MIT
"""Export traceable connection records as a deterministic CSV schedule."""

from pathlib import Path

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.connections import connection_schedule_csv, connections_from_project


def connection_schedule_csv_for_objects(objects) -> str:
    records = []
    for obj in objects:
        if hasattr(obj, "ProjectId") and hasattr(obj, "ConnectionRecords"):
            records.extend(connections_from_project(obj))
    return connection_schedule_csv(records)


class ExportConnectionScheduleCommand:
    def GetResources(self):
        return {"MenuText": "Export Connection Schedule", "ToolTip": "Export signal-to-terminal-to-wire connection records to CSV."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        output_path = Path.home() / "integracad_connection_schedule.csv"
        output_path.write_text(connection_schedule_csv_for_objects(App.ActiveDocument.Objects), encoding="utf-8")
        App.Console.PrintMessage(f"Connection schedule exported to {output_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportConnectionSchedule", ExportConnectionScheduleCommand())

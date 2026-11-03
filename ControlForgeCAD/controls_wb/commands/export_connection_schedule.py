# SPDX-License-Identifier: MIT
"""Export traceable connection records as a deterministic CSV schedule."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.connections import connection_schedule_csv, connections_from_project
from controls_wb.project_workspace import ProjectWorkspaceError, export_destination_for_objects


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
        try:
            output_path = export_destination_for_objects(App.ActiveDocument.Objects, "schedules", "integracad_connection_schedule.csv")
        except ProjectWorkspaceError as exc:
            App.Console.PrintWarning(f"Connection schedule was not exported: {exc}\n")
            return
        output_path.write_text(connection_schedule_csv_for_objects(App.ActiveDocument.Objects), encoding="utf-8")
        App.Console.PrintMessage(f"Connection schedule exported to {output_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportConnectionSchedule", ExportConnectionScheduleCommand())

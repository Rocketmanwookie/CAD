# SPDX-License-Identifier: MIT
"""Export a starter controls I/O list CSV."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.io_list import io_list_csv, io_mapping_summary, io_signals_from_objects
from controls_wb.project_workspace import ProjectWorkspaceError, export_destination_for_objects


def io_list_csv_for_objects(objects) -> str:
    signals = io_signals_from_objects(list(objects))
    return io_list_csv(signals)


class ExportIOListCommand:
    def GetResources(self):
        return {
            "MenuText": "Export I/O List",
            "ToolTip": "Export a starter controls I/O list CSV.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        signals = io_signals_from_objects(App.ActiveDocument.Objects)
        try:
            output_path = export_destination_for_objects(App.ActiveDocument.Objects, "io", "integracab_io_list.csv")
        except ProjectWorkspaceError as exc:
            App.Console.PrintWarning(f"I/O list was not exported: {exc}\n")
            return
        output_path.write_text(io_list_csv(signals), encoding="utf-8")
        summary = io_mapping_summary(signals)
        if summary:
            App.Console.PrintMessage(f"{summary}\n")
        App.Console.PrintMessage(f"I/O list exported to {output_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportIOList", ExportIOListCommand())

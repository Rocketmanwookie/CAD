# SPDX-License-Identifier: MIT
"""Export the controls project missing-data matrix CSV."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.commands.missing_data import missing_data_rows_for_objects
from controls_wb.missing_data import missing_data_csv
from controls_wb.project_workspace import ProjectWorkspaceError, export_destination_for_objects


def missing_data_csv_for_objects(objects) -> str:
    return missing_data_csv(missing_data_rows_for_objects(objects))


class ExportMissingDataCSVCommand:
    def GetResources(self):
        return {
            "MenuText": "Export Missing Data CSV",
            "ToolTip": "Export the controls project missing-data matrix to CSV.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        rows = missing_data_rows_for_objects(App.ActiveDocument.Objects)
        try:
            output_path = export_destination_for_objects(App.ActiveDocument.Objects, "reports", "integracab_missing_data.csv")
        except ProjectWorkspaceError as exc:
            App.Console.PrintWarning(f"Missing-data CSV was not exported: {exc}\n")
            return
        output_path.write_text(missing_data_csv(rows), encoding="utf-8")
        App.Console.PrintMessage(f"Missing-data CSV exported to {output_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportMissingDataCSV", ExportMissingDataCSVCommand())

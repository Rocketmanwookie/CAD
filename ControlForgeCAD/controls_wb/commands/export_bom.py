# SPDX-License-Identifier: MIT
"""Export a simple controls BOM CSV from FreeCAD document objects."""

import csv

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.project_workspace import ProjectWorkspaceError, export_destination_for_objects


def collect_bom_rows(objects):
    rows = []
    for obj in objects:
        if not any(hasattr(obj, attr) for attr in ["Tag", "Description", "Manufacturer", "PartNumber"]):
            continue
        rows.append({
            "Tag": getattr(obj, "Tag", ""),
            "Description": getattr(obj, "Description", ""),
            "Manufacturer": getattr(obj, "Manufacturer", ""),
            "PartNumber": getattr(obj, "PartNumber", ""),
            "Quantity": 1,
        })
    return rows


class ExportBOMCommand:
    def GetResources(self):
        return {"MenuText": "Export BOM", "ToolTip": "Export controls components to a CSV BOM."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        rows = collect_bom_rows(App.ActiveDocument.Objects)
        try:
            output_path = export_destination_for_objects(App.ActiveDocument.Objects, "bom", "controlforgecad_bom.csv")
        except ProjectWorkspaceError as exc:
            App.Console.PrintWarning(f"BOM was not exported: {exc}\n")
            return
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Tag", "Description", "Manufacturer", "PartNumber", "Quantity"])
            writer.writeheader()
            writer.writerows(rows)
        App.Console.PrintMessage(f"BOM exported to {output_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportBOM", ExportBOMCommand())

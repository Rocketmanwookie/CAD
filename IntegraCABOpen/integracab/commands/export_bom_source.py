# SPDX-License-Identifier: MIT
"""Export BOM-source rows for external BOM tools."""

import csv
from pathlib import Path

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None


def collect_bom_source_rows(objects):
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
            "SourceSystem": "IntegraCABOpen",
            "ExportPurpose": "BOMSource",
        })
    return rows


class ExportBOMSourceCommand:
    def GetResources(self):
        return {"MenuText": "Export BOM Source", "ToolTip": "Export normalized source rows for external BOM tools."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        rows = collect_bom_source_rows(App.ActiveDocument.Objects)
        output_path = Path.home() / "integracab_bom_source.csv"
        with output_path.open("w", newline="", encoding="utf-8") as f:
            fieldnames = ["Tag", "Description", "Manufacturer", "PartNumber", "Quantity", "SourceSystem", "ExportPurpose"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        App.Console.PrintMessage(f"BOM source exported to {output_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("ICAB_ExportBOMSource", ExportBOMSourceCommand())

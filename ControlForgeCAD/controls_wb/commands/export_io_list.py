# SPDX-License-Identifier: MIT
"""Export a starter controls I/O list CSV."""

from pathlib import Path

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.io_list import io_list_csv, io_signals_from_objects, unmapped_io_findings


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
        output_path = Path.home() / "integracab_io_list.csv"
        output_path.write_text(io_list_csv(signals), encoding="utf-8")
        for finding in unmapped_io_findings(signals):
            App.Console.PrintMessage(f"{finding}\n")
        App.Console.PrintMessage(f"I/O list exported to {output_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportIOList", ExportIOListCommand())

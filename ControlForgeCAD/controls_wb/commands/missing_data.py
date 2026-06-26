# SPDX-License-Identifier: MIT
"""Preview the controls project missing-data matrix."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.missing_data import MissingDataRow, missing_data_matrix


def project_objects(objects):
    return [
        obj
        for obj in objects
        if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables")
    ]


def missing_data_rows_for_objects(objects) -> list[MissingDataRow]:
    rows: list[MissingDataRow] = []
    for project in project_objects(objects):
        rows.extend(missing_data_matrix(project))
    return rows


def format_missing_data_rows(rows: list[MissingDataRow]) -> list[str]:
    if not rows:
        return ["INFO: No controls project intake object found."]
    return [
        (
            f"{row.severity.upper()}: {row.fact_id} [{row.status}] "
            f"{row.finding} Next: {row.next_action}"
        )
        for row in rows
    ]


class MissingDataCommand:
    def GetResources(self):
        return {
            "MenuText": "Preview Missing Data",
            "ToolTip": "Preview the missing-data matrix for controls project intake.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        for line in format_missing_data_rows(missing_data_rows_for_objects(App.ActiveDocument.Objects)):
            App.Console.PrintMessage(f"{line}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_PreviewMissingData", MissingDataCommand())

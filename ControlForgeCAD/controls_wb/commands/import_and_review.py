# SPDX-License-Identifier: MIT
"""Import supported project data through an explicit review gate."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.freecad_transactions import document_transaction
from controls_wb.gui.import_review import choose_staged_project_import
from controls_wb.gui.project_intake import existing_project_object
from controls_wb.import_review import ImportReviewError, apply_approved_project_import
from controls_wb.model.project import create_or_update_project


class ImportAndReviewCommand:
    """FreeCAD boundary that stages, reviews, then atomically applies project data."""

    def GetResources(self):
        return {
            "MenuText": "Import and Review Project Data",
            "ToolTip": "Preview CEProject XML or setup YAML/UML data and apply only approved fields.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        try:
            parent = Gui.getMainWindow() if Gui is not None and hasattr(Gui, "getMainWindow") else None
            decision = choose_staged_project_import(App.ActiveDocument, parent)
            if decision is None:
                return
            staged, approved_keys = decision
            with document_transaction(App.ActiveDocument, "Import and review project data"):
                project = existing_project_object(App.ActiveDocument) or create_or_update_project(App.ActiveDocument)
                apply_approved_project_import(project, staged, approved_keys)
                App.ActiveDocument.recompute()
        except (ImportReviewError, RuntimeError, ValueError) as exc:
            App.Console.PrintWarning(f"Project import was not applied: {exc}\n")
            return
        App.Console.PrintMessage(f"Imported {len(approved_keys)} approved project field(s).\n")

    def IsActive(self):
        return App is not None


if Gui is not None:
    Gui.addCommand("CE_ImportAndReview", ImportAndReviewCommand())

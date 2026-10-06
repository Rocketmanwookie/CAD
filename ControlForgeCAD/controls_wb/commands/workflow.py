# SPDX-License-Identifier: MIT
"""Workflow entry points using the same persisted CE_Project."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.freecad_transactions import document_transaction
from controls_wb.gui.project_intake import existing_project_object
from controls_wb.gui.workflow import show_io_count_dialog, show_plant_questionnaire


class PlantQuestionnaireCommand:
    def GetResources(self):
        return {"MenuText": "Plant Questionnaire", "ToolTip": "Define plant and project facts before I/O sizing."}

    def IsActive(self):
        return App is not None

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        _run_step(show_plant_questionnaire, "Plant Questionnaire")


class IOCountCommand:
    def GetResources(self):
        return {"MenuText": "I/O Count", "ToolTip": "Enter actual DI/DO/AI/AO demand and review 20% spare capacity."}

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None and existing_project_object(App.ActiveDocument) is not None

    def Activated(self):
        _run_step(show_io_count_dialog, "I/O Count")


def _run_step(show_dialog, title):
    try:
        parent = Gui.getMainWindow() if Gui is not None else None
        with document_transaction(App.ActiveDocument, title):
            project = show_dialog(App.ActiveDocument, parent)
            if project is not None:
                App.ActiveDocument.recompute()
                App.Console.PrintMessage(f"{title} saved: {project.ProjectName}\n")
    except (ValueError, RuntimeError) as exc:
        App.Console.PrintWarning(f"{title}: {exc}\n")


if Gui is not None:
    Gui.addCommand("CE_PlantQuestionnaire", PlantQuestionnaireCommand())
    Gui.addCommand("CE_IOCount", IOCountCommand())

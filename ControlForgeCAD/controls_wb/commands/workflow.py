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
from controls_wb.gui.workflow import show_io_count_dialog, show_plant_questionnaire, show_plc_configurator, show_define_io


class PlantQuestionnaireCommand:
    def GetResources(self):
        return {
            "MenuText": "Send Job Intake Form",
            "ToolTip": "Prepare the job intake form for a client or project contact.",
            "Pixmap": "send-intake.svg",
        }

    def IsActive(self):
        return App is not None

    def Activated(self):
        if App.ActiveDocument is None:
            App.newDocument("ControlsProject")
        _run_step(show_plant_questionnaire, "Job Intake Form")


class IOCountCommand:
    def GetResources(self):
        return {"MenuText": "I/O Count", "ToolTip": "Enter actual DI/DO/AI/AO demand and review 20% spare capacity."}

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None and existing_project_object(App.ActiveDocument) is not None

    def Activated(self):
        _run_step(show_io_count_dialog, "I/O Count")


class PLCConfiguratorCommand(IOCountCommand):
    def GetResources(self):
        return {
            "MenuText": "PLC Configuration",
            "ToolTip": "Review the PLC CPU, I/O modules, and communications modules before allocation.",
            "Pixmap": "plc-configuration.svg",
        }

    def Activated(self):
        _run_step(show_plc_configurator, "PLC Configuration")


class DefineIOCommand(IOCountCommand):
    def GetResources(self):
        return {
            "MenuText": "Define I/O",
            "ToolTip": "Label configured I/O points while retaining catalog channel assignments.",
            "Pixmap": "define-io.svg",
        }

    def Activated(self):
        _run_step(show_define_io, "Define I/O")


class IntakeConsoleCommand:
    """Open the existing review-gated project import flow as the database console."""

    def GetResources(self):
        return {
            "MenuText": "Open Job Database Console",
            "ToolTip": "Review incoming project data and apply only the fields you approve.",
            "Pixmap": "database-console.svg",
        }

    def IsActive(self):
        return App is not None

    def Activated(self):
        # Keep the command boundary centralized: the import/review command
        # already stages incoming data and requires explicit field approval.
        from controls_wb.commands.import_and_review import ImportAndReviewCommand

        ImportAndReviewCommand().Activated()


class IntakeSystemSettingsCommand:
    """Provide an icon-first entry point for intake/database setup."""

    def GetResources(self):
        return {
            "MenuText": "Job Intake & Database Settings",
            "ToolTip": "Configure the local job-intake database and form-delivery integration.",
            "Pixmap": "settings.svg",
        }

    def IsActive(self):
        return App is not None

    def Activated(self):
        from controls_wb.intake_settings import show_intake_system_settings

        parent = Gui.getMainWindow() if Gui is not None and hasattr(Gui, "getMainWindow") else None
        show_intake_system_settings(parent)


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
    Gui.addCommand("CE_PLCConfigurator", PLCConfiguratorCommand())
    Gui.addCommand("CE_DefineIO", DefineIOCommand())
    Gui.addCommand("CE_SendIntakeForm", PlantQuestionnaireCommand())
    Gui.addCommand("CE_OpenIntakeConsole", IntakeConsoleCommand())
    Gui.addCommand("CE_IntakeSystemSettings", IntakeSystemSettingsCommand())

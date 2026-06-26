# SPDX-License-Identifier: MIT
"""Run first-pass controls project validation."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.intake import validate_intake
from controls_wb.missing_data import project_object_to_intake


def validate_project_objects(objects):
    messages = []
    for obj in objects:
        if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables"):
            for finding in validate_intake(project_object_to_intake(obj)):
                ask_suffix = f" Ask: {finding.ask}." if finding.ask else ""
                messages.append((finding.level, f"{finding.message}{ask_suffix}"))
    return messages


def validate_document_objects(objects):
    messages = validate_project_objects(objects)
    seen_tags = set()
    for obj in objects:
        tag = getattr(obj, "Tag", "") if hasattr(obj, "Tag") else ""
        part_number = getattr(obj, "PartNumber", "") if hasattr(obj, "PartNumber") else ""
        description = getattr(obj, "Description", "") if hasattr(obj, "Description") else ""
        if tag:
            if tag in seen_tags:
                messages.append(("ERROR", f"Duplicate tag: {tag}"))
            seen_tags.add(tag)
            if not part_number:
                messages.append(("WARNING", f"{tag} has no part number assigned."))
            if not description:
                messages.append(("WARNING", f"{tag} has no description assigned."))
    if not messages:
        messages.append(("INFO", "No validation messages."))
    return messages


class ValidateProjectCommand:
    def GetResources(self):
        return {"MenuText": "Validate Controls Project", "ToolTip": "Check tags and controls metadata completeness."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        for level, message in validate_document_objects(App.ActiveDocument.Objects):
            App.Console.PrintMessage(f"{level}: {message}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ValidateProject", ValidateProjectCommand())

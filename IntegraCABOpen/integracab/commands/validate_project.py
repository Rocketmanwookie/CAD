# SPDX-License-Identifier: MIT
"""Run first-pass controls project validation."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None


def validate_document_objects(objects):
    messages = []
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
        return {"MenuText": "Validate Project", "ToolTip": "Check controls metadata completeness."}

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        for level, message in validate_document_objects(App.ActiveDocument.Objects):
            App.Console.PrintMessage(f"{level}: {message}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("ICAB_ValidateProject", ValidateProjectCommand())

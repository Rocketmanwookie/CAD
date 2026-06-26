# SPDX-License-Identifier: MIT
"""Run first-pass controls project validation."""

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.intake import FieldStatus, IntakeField, ProjectIntake, validate_intake


def _status(value):
    try:
        return FieldStatus(value)
    except ValueError:
        return FieldStatus.UNKNOWN


def _intake_from_project_object(obj):
    fields = {
        "project.name": IntakeField(
            "project.name",
            "Project name",
            "Project manager",
            value=getattr(obj, "ProjectName", ""),
            status=FieldStatus.RECEIVED if getattr(obj, "ProjectName", "") else FieldStatus.UNKNOWN,
        ),
        "powerFeed.nominalVoltage": IntakeField(
            "powerFeed.nominalVoltage",
            "Nominal voltage",
            "Electrical engineering",
            status=_status(getattr(obj, "PowerFeedStatus", "")),
        ),
        "powerFeed.phaseCount": IntakeField(
            "powerFeed.phaseCount",
            "Phase count",
            "Electrical engineering",
            status=_status(getattr(obj, "PowerFeedStatus", "")),
        ),
        "controls.plcPlatform": IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            status=_status(getattr(obj, "PlcPlatformStatus", "")),
        ),
        "io.sensorCount": IntakeField(
            "io.sensorCount",
            "Sensor count or estimate",
            "Mechanical / materials handling",
            status=_status(getattr(obj, "SensorCountStatus", "")),
        ),
    }
    return ProjectIntake(
        project_id=getattr(obj, "ProjectId", "CE-PROJECT-001"),
        name=getattr(obj, "ProjectName", "Controls Project"),
        schema_version=getattr(obj, "SchemaVersion", "0.1.0"),
        fields=fields,
        deliverables=set(getattr(obj, "Deliverables", [])),
    )


def validate_project_objects(objects):
    messages = []
    for obj in objects:
        if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables"):
            for finding in validate_intake(_intake_from_project_object(obj)):
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

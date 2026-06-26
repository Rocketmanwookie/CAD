# SPDX-License-Identifier: MIT
"""Run first-pass controls project validation."""

import json

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

from controls_wb.intake import (
    Contact,
    FieldStatus,
    IntakeField,
    IntakeQuestionResponse,
    ProjectIntake,
    SourceRecord,
    SourceRecordType,
    validate_intake,
)


def _status(value):
    try:
        return FieldStatus(value)
    except ValueError:
        return FieldStatus.UNKNOWN


def _json_records(obj, attribute):
    records = []
    for item in getattr(obj, attribute, []) or []:
        try:
            records.append(json.loads(item))
        except (TypeError, ValueError):
            continue
    return records


def _contacts_from_project_object(obj):
    contacts = {}
    for record in _json_records(obj, "Contacts"):
        contact_id = record.get("id", "")
        if contact_id:
            contacts[contact_id] = Contact(
                contact_id=contact_id,
                role=record.get("role", ""),
                name=record.get("name", ""),
                email=record.get("email", ""),
                organization=record.get("organization", ""),
            )
    return contacts


def _sources_from_project_object(obj):
    sources = {}
    for record in _json_records(obj, "SourceRecords"):
        source_id = record.get("id", "")
        if source_id:
            try:
                source_type = SourceRecordType(record.get("type", "manual_entry"))
            except ValueError:
                source_type = SourceRecordType.MANUAL_ENTRY
            sources[source_id] = SourceRecord(
                source_id=source_id,
                source_type=source_type,
                title=record.get("title", ""),
                stakeholder=record.get("stakeholder", ""),
                field_ids=tuple(record.get("fieldIds", ())),
                reference=record.get("reference", ""),
                received_on=record.get("receivedOn", ""),
            )
    return sources


def _questions_from_project_object(obj):
    questions = {}
    for record in _json_records(obj, "IntakeQuestions"):
        question_id = record.get("id", "")
        if question_id:
            questions[question_id] = IntakeQuestionResponse(
                question_id=question_id,
                field_id=record.get("fieldId", ""),
                prompt=record.get("prompt", ""),
                ask=record.get("ask", ""),
                status=_status(record.get("status", "")),
                response=record.get("response", ""),
                source_ids=tuple(record.get("sourceIds", ())),
            )
    return questions


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
            value=getattr(obj, "NominalVoltage", ""),
            status=_status(getattr(obj, "PowerFeedStatus", "")),
        ),
        "powerFeed.phaseCount": IntakeField(
            "powerFeed.phaseCount",
            "Phase count",
            "Electrical engineering",
            value=getattr(obj, "PhaseCount", ""),
            status=_status(getattr(obj, "PowerFeedStatus", "")),
        ),
        "controls.plcPlatform": IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value=getattr(obj, "PlcPlatform", ""),
            status=_status(getattr(obj, "PlcPlatformStatus", "")),
        ),
        "io.sensorCount": IntakeField(
            "io.sensorCount",
            "Sensor count or estimate",
            "Mechanical / materials handling",
            value=getattr(obj, "SensorCount", ""),
            status=_status(getattr(obj, "SensorCountStatus", "")),
        ),
    }
    return ProjectIntake(
        project_id=getattr(obj, "ProjectId", "CE-PROJECT-001"),
        name=getattr(obj, "ProjectName", "Controls Project"),
        schema_version=getattr(obj, "SchemaVersion", "0.1.0"),
        fields=fields,
        deliverables=set(getattr(obj, "Deliverables", [])),
        contacts=_contacts_from_project_object(obj),
        source_records=_sources_from_project_object(obj),
        questions=_questions_from_project_object(obj),
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

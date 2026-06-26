# SPDX-License-Identifier: MIT
"""FreeCAD project/intake object wrapper."""

import json

try:
    import FreeCAD as App
except Exception:  # pragma: no cover
    App = None

from controls_wb.intake import SCHEMA_VERSION, default_project_intake


def _project_payloads(intake):
    contacts = [
        json.dumps(
            {
                "id": contact.contact_id,
                "role": contact.role,
                "name": contact.name,
                "email": contact.email,
                "organization": contact.organization,
            },
            sort_keys=True,
        )
        for contact in intake.contacts.values()
    ]
    sources = [
        json.dumps(
            {
                "id": source.source_id,
                "type": source.source_type.value,
                "title": source.title,
                "stakeholder": source.stakeholder,
                "fieldIds": list(source.field_ids),
                "reference": source.reference,
                "receivedOn": source.received_on,
            },
            sort_keys=True,
        )
        for source in intake.source_records.values()
    ]
    questions = [
        json.dumps(
            {
                "id": question.question_id,
                "fieldId": question.field_id,
                "prompt": question.prompt,
                "ask": question.ask,
                "status": question.status.value,
                "response": question.response,
                "sourceIds": list(question.source_ids),
            },
            sort_keys=True,
        )
        for question in intake.questions.values()
    ]
    return contacts, sources, questions


def create_project(name: str = "Controls Project"):
    """Create a lightweight CEProject object in the active FreeCAD document."""
    obj = App.ActiveDocument.addObject("App::FeaturePython", "CE_Project")
    ControlsProject(obj)
    intake = default_project_intake(name=name)
    contacts, sources, questions = _project_payloads(intake)
    obj.ProjectId = intake.project_id
    obj.ProjectName = intake.name
    obj.SchemaVersion = intake.schema_version
    obj.Deliverables = sorted(intake.deliverables)
    obj.Contacts = contacts
    obj.SourceRecords = sources
    obj.IntakeQuestions = questions
    obj.NominalVoltage = ""
    obj.PhaseCount = ""
    obj.EnclosureRating = ""
    obj.PlcPlatform = ""
    obj.SensorCount = ""
    obj.PowerFeedStatus = "Requested"
    obj.EnclosureRatingStatus = "Requested"
    obj.PlcPlatformStatus = "Requested"
    obj.SensorCountStatus = "Requested"
    return obj


class ControlsProject:
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "ControlsProject"
        obj.addProperty("App::PropertyString", "ProjectId", "CEProject", "CEProject identifier")
        obj.addProperty("App::PropertyString", "ProjectName", "CEProject", "Project name")
        obj.addProperty("App::PropertyString", "SchemaVersion", "CEProject", "CEProject schema version")
        obj.addProperty("App::PropertyStringList", "Deliverables", "Intake", "Selected deliverables")
        obj.addProperty("App::PropertyStringList", "Contacts", "Intake", "Stakeholder contact records as JSON lines")
        obj.addProperty("App::PropertyStringList", "SourceRecords", "Intake", "Source records as JSON lines")
        obj.addProperty("App::PropertyStringList", "IntakeQuestions", "Intake", "Question and response records as JSON lines")
        obj.addProperty("App::PropertyString", "NominalVoltage", "Intake", "Nominal voltage response")
        obj.addProperty("App::PropertyString", "PhaseCount", "Intake", "Phase count response")
        obj.addProperty("App::PropertyString", "EnclosureRating", "Intake", "Enclosure rating response")
        obj.addProperty("App::PropertyString", "PlcPlatform", "Intake", "PLC platform response")
        obj.addProperty("App::PropertyString", "SensorCount", "Intake", "Sensor count response")
        obj.addProperty("App::PropertyString", "PowerFeedStatus", "Intake", "Power feed intake status")
        obj.addProperty("App::PropertyString", "EnclosureRatingStatus", "Intake", "Enclosure rating intake status")
        obj.addProperty("App::PropertyString", "PlcPlatformStatus", "Intake", "PLC platform intake status")
        obj.addProperty("App::PropertyString", "SensorCountStatus", "Intake", "Sensor count intake status")

    def execute(self, obj):
        return None

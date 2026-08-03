# SPDX-License-Identifier: MIT
"""FreeCAD project/intake object wrapper."""

import json
from dataclasses import dataclass

try:
    import FreeCAD as App
except Exception:  # pragma: no cover
    App = None

from controls_wb.intake import SCHEMA_VERSION, ProjectIntake, default_project_intake


@dataclass(frozen=True)
class ProjectPropertySpec:
    property_type: str
    name: str
    group: str
    description: str


PROJECT_PROPERTY_SPECS = (
    ProjectPropertySpec("App::PropertyString", "ProjectId", "CEProject", "CEProject identifier"),
    ProjectPropertySpec("App::PropertyString", "ProjectName", "CEProject", "Project name"),
    ProjectPropertySpec("App::PropertyString", "Customer", "CEProject", "Customer name"),
    ProjectPropertySpec("App::PropertyString", "SiteLocation", "CEProject", "Site or installation location"),
    ProjectPropertySpec("App::PropertyString", "SchemaVersion", "CEProject", "CEProject schema version"),
    ProjectPropertySpec("App::PropertyStringList", "CEProjectImports", "CEProject", "Remembered CEProject XML import records as JSON lines"),
    ProjectPropertySpec("App::PropertyStringList", "Deliverables", "Intake", "Selected deliverables"),
    ProjectPropertySpec("App::PropertyStringList", "Contacts", "Intake", "Stakeholder contact records as JSON lines"),
    ProjectPropertySpec("App::PropertyStringList", "SourceRecords", "Intake", "Source records as JSON lines"),
    ProjectPropertySpec("App::PropertyStringList", "IntakeQuestions", "Intake", "Question and response records as JSON lines"),
    ProjectPropertySpec("App::PropertyStringList", "IOSignals", "I/O", "Explicit I/O signal records as JSON lines"),
    ProjectPropertySpec("App::PropertyString", "NominalVoltage", "Intake", "Nominal voltage response"),
    ProjectPropertySpec("App::PropertyString", "PhaseCount", "Intake", "Phase count response"),
    ProjectPropertySpec("App::PropertyString", "PowerConfiguration", "Power", "Combined phase and voltage"),
    ProjectPropertySpec("App::PropertyString", "EnclosureRating", "Intake", "Enclosure rating response"),
    ProjectPropertySpec("App::PropertyStringList", "EnclosureRatings", "Intake", "Selected enclosure ratings"),
    ProjectPropertySpec("App::PropertyString", "PlcMake", "PLC / I/O", "PLC manufacturer"),
    ProjectPropertySpec("App::PropertyString", "PlcLine", "PLC / I/O", "PLC product line"),
    ProjectPropertySpec("App::PropertyString", "PlcCPU", "PLC / I/O", "PLC CPU selection"),
    ProjectPropertySpec("App::PropertyString", "PlcPlatform", "Intake", "PLC platform response"),
    ProjectPropertySpec("App::PropertyString", "SensorCount", "Intake", "Sensor count response"),
    ProjectPropertySpec("App::PropertyString", "DICount", "PLC / I/O", "Digital input count"),
    ProjectPropertySpec("App::PropertyString", "DOCount", "PLC / I/O", "Digital output count"),
    ProjectPropertySpec("App::PropertyString", "AICount", "PLC / I/O", "Analog input count"),
    ProjectPropertySpec("App::PropertyString", "AOCount", "PLC / I/O", "Analog output count"),
    ProjectPropertySpec("App::PropertyStringList", "IOAccessories", "PLC / I/O", "Selected I/O accessories"),
    ProjectPropertySpec("App::PropertyString", "EthernetAdapter", "PLC / I/O", "Compatible Ethernet adapter"),
    ProjectPropertySpec("App::PropertyString", "ExpansionPowerSupply", "PLC / I/O", "Compatible expansion power supply"),
    ProjectPropertySpec("App::PropertyString", "IOExpansionSuggestion", "PLC / I/O", "I/O expansion planning suggestion"),
    ProjectPropertySpec("App::PropertyStringList", "CommunicationProtocols", "PLC / I/O", "Selected communication protocols"),
    ProjectPropertySpec("App::PropertyString", "PowerFeedStatus", "Intake", "Power feed intake status"),
    ProjectPropertySpec("App::PropertyString", "EnclosureRatingStatus", "Intake", "Enclosure rating intake status"),
    ProjectPropertySpec("App::PropertyString", "PlcPlatformStatus", "Intake", "PLC platform intake status"),
    ProjectPropertySpec("App::PropertyString", "SensorCountStatus", "Intake", "Sensor count intake status"),
)


def _project_payloads(intake: ProjectIntake) -> tuple[list[str], list[str], list[str]]:
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


def intake_to_project_properties(intake: ProjectIntake) -> dict[str, object]:
    """Return editable FreeCAD property values for a project intake."""
    contacts, sources, questions = _project_payloads(intake)
    return {
        "ProjectId": intake.project_id,
        "ProjectName": intake.name,
        "Customer": "",
        "SiteLocation": "",
        "SchemaVersion": intake.schema_version,
        "CEProjectImports": [],
        "Deliverables": sorted(intake.deliverables),
        "Contacts": contacts,
        "SourceRecords": sources,
        "IntakeQuestions": questions,
        "IOSignals": [],
        "NominalVoltage": intake.fields.get("powerFeed.nominalVoltage", "").value
        if "powerFeed.nominalVoltage" in intake.fields
        else "",
        "PhaseCount": intake.fields.get("powerFeed.phaseCount", "").value
        if "powerFeed.phaseCount" in intake.fields
        else "",
        "PowerConfiguration": "",
        "EnclosureRating": intake.fields.get("environment.enclosureRating", "").value
        if "environment.enclosureRating" in intake.fields
        else "",
        "EnclosureRatings": [],
        "PlcMake": "",
        "PlcLine": "",
        "PlcCPU": "",
        "PlcPlatform": intake.fields.get("controls.plcPlatform", "").value
        if "controls.plcPlatform" in intake.fields
        else "",
        "SensorCount": intake.fields.get("io.sensorCount", "").value
        if "io.sensorCount" in intake.fields
        else "",
        "DICount": "",
        "DOCount": "",
        "AICount": "",
        "AOCount": "",
        "IOAccessories": [],
        "EthernetAdapter": "",
        "ExpansionPowerSupply": "",
        "IOExpansionSuggestion": "",
        "CommunicationProtocols": [],
        "PowerFeedStatus": "Requested",
        "EnclosureRatingStatus": "Requested",
        "PlcPlatformStatus": "Requested",
        "SensorCountStatus": "Requested",
    }


def ensure_project_properties(obj) -> None:
    """Add the editable CE_Project property set to a FreeCAD-like object."""
    existing = set(getattr(obj, "PropertiesList", []) or [])
    for spec in PROJECT_PROPERTY_SPECS:
        if spec.name not in existing:
            obj.addProperty(spec.property_type, spec.name, spec.group, spec.description)


def apply_project_properties(obj, properties: dict[str, object]) -> None:
    for name, value in properties.items():
        setattr(obj, name, value)


def initialize_project_object(obj, intake: ProjectIntake) -> object:
    ControlsProject(obj)
    apply_project_properties(obj, intake_to_project_properties(intake))
    return obj


def create_project(name: str = "Controls Project"):
    """Create an editable CEProject object in the active FreeCAD document."""
    obj = App.ActiveDocument.addObject("App::FeaturePython", "CE_Project")
    return initialize_project_object(obj, default_project_intake(name=name))


def is_controls_project_object(obj) -> bool:
    return hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables")


def controls_project_objects(objects) -> list[object]:
    return [obj for obj in objects if is_controls_project_object(obj)]


def create_or_update_project(document, name: str = "Controls Project"):
    """Create or refresh the first editable CE_Project object in a document."""
    projects = controls_project_objects(getattr(document, "Objects", []) or [])
    if projects:
        return initialize_project_object(projects[0], default_project_intake(name=name))
    obj = document.addObject("App::FeaturePython", "CE_Project")
    return initialize_project_object(obj, default_project_intake(name=name))


class ControlsProject:
    def __init__(self, obj):
        obj.Proxy = self
        self.Type = "ControlsProject"
        ensure_project_properties(obj)

    def execute(self, obj):
        return None

    def __getstate__(self):
        return {"Type": self.Type}

    def __setstate__(self, state):
        self.Type = state.get("Type", "ControlsProject")

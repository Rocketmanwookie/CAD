# SPDX-License-Identifier: MIT
"""Pure-Python project intake model and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


SCHEMA_VERSION = "0.1.0"


class FieldStatus(str, Enum):
    UNKNOWN = "Unknown"
    REQUESTED = "Requested"
    RECEIVED = "Received"
    ASSUMED = "Assumed"
    ESTIMATED = "Estimated"
    VERIFIED = "Verified"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    SUPERSEDED = "Superseded"


class SourceRecordType(str, Enum):
    EMAIL = "email"
    MEETING_NOTE = "meeting_note"
    UPLOADED_FILE = "uploaded_file"
    PHONE_CALL = "phone_call"
    FIELD_NOTE = "field_note"
    VENDOR_QUOTE = "vendor_quote"
    CADBASE_ASSET = "cadbase_asset"
    BIM_OBJECT = "bim_object"
    MANUAL_ENTRY = "manual_entry"


@dataclass(frozen=True)
class Contact:
    contact_id: str
    role: str
    name: str = ""
    email: str = ""
    organization: str = ""


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    source_type: SourceRecordType
    title: str
    stakeholder: str
    field_ids: tuple[str, ...] = ()
    reference: str = ""
    received_on: str = ""


@dataclass(frozen=True)
class IntakeQuestionResponse:
    question_id: str
    field_id: str
    prompt: str
    ask: str
    status: FieldStatus = FieldStatus.REQUESTED
    response: str = ""
    source_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class IntakeField:
    field_id: str
    label: str
    stakeholder: str
    value: str = ""
    status: FieldStatus = FieldStatus.UNKNOWN


@dataclass(frozen=True)
class ValidationFinding:
    level: str
    field_id: str
    message: str
    ask: str = ""


@dataclass
class ProjectIntake:
    project_id: str
    name: str
    schema_version: str = SCHEMA_VERSION
    fields: dict[str, IntakeField] = field(default_factory=dict)
    deliverables: set[str] = field(default_factory=set)
    contacts: dict[str, Contact] = field(default_factory=dict)
    source_records: dict[str, SourceRecord] = field(default_factory=dict)
    questions: dict[str, IntakeQuestionResponse] = field(default_factory=dict)


REQUIRED_FIELDS_BY_DELIVERABLE: dict[str, tuple[IntakeField, ...]] = {
    "panelLayout": (
        IntakeField("project.name", "Project name", "Project manager"),
        IntakeField("powerFeed.nominalVoltage", "Nominal voltage", "Electrical engineering"),
        IntakeField("powerFeed.phaseCount", "Phase count", "Electrical engineering"),
        IntakeField("environment.enclosureRating", "Enclosure rating", "Operations / maintenance"),
    ),
    "ioList": (
        IntakeField("project.name", "Project name", "Project manager"),
        IntakeField("controls.plcPlatform", "PLC platform", "Controls lead"),
        IntakeField("io.sensorCount", "Sensor count or estimate", "Mechanical / materials handling"),
    ),
    "bomSourceExport": (
        IntakeField("project.name", "Project name", "Project manager"),
        IntakeField("purchasing.preferredVendors", "Preferred vendors", "Purchasing"),
        IntakeField("costing.budgetStatus", "Budget or quote status", "Sales / estimator"),
    ),
}


def default_project_intake(project_id: str = "CE-PROJECT-001", name: str = "Controls Project") -> ProjectIntake:
    """Create the starter intake used by the first FreeCAD project command."""
    source_id = "SRC-MANUAL-001"
    fields = {
        "project.name": IntakeField(
            "project.name",
            "Project name",
            "Project manager",
            value=name,
            status=FieldStatus.RECEIVED,
        ),
        "powerFeed.nominalVoltage": IntakeField(
            "powerFeed.nominalVoltage",
            "Nominal voltage",
            "Electrical engineering",
            status=FieldStatus.REQUESTED,
        ),
        "powerFeed.phaseCount": IntakeField(
            "powerFeed.phaseCount",
            "Phase count",
            "Electrical engineering",
            status=FieldStatus.REQUESTED,
        ),
        "environment.enclosureRating": IntakeField(
            "environment.enclosureRating",
            "Enclosure rating",
            "Operations / maintenance",
            status=FieldStatus.REQUESTED,
        ),
        "controls.plcPlatform": IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            status=FieldStatus.REQUESTED,
        ),
        "io.sensorCount": IntakeField(
            "io.sensorCount",
            "Sensor count or estimate",
            "Mechanical / materials handling",
            status=FieldStatus.REQUESTED,
        ),
    }
    contacts = {
        "project_manager": Contact("project_manager", "Project manager"),
        "electrical_engineering": Contact("electrical_engineering", "Electrical engineering"),
        "controls_lead": Contact("controls_lead", "Controls lead"),
        "mechanical_materials_handling": Contact(
            "mechanical_materials_handling",
            "Mechanical / materials handling",
        ),
        "operations_maintenance": Contact("operations_maintenance", "Operations / maintenance"),
    }
    source_records = {
        source_id: SourceRecord(
            source_id,
            SourceRecordType.MANUAL_ENTRY,
            "Starter project creation",
            "Project manager",
            field_ids=("project.name",),
        )
    }
    questions = _starter_questions(fields)
    return ProjectIntake(
        project_id=project_id,
        name=name,
        fields=fields,
        deliverables={"panelLayout", "ioList"},
        contacts=contacts,
        source_records=source_records,
        questions=questions,
    )


def required_fields_for(deliverables: Iterable[str]) -> dict[str, IntakeField]:
    required: dict[str, IntakeField] = {}
    for deliverable in sorted(deliverables):
        for intake_field in REQUIRED_FIELDS_BY_DELIVERABLE.get(deliverable, ()):
            required.setdefault(intake_field.field_id, intake_field)
    return required


def _starter_questions(fields: dict[str, IntakeField]) -> dict[str, IntakeQuestionResponse]:
    questions: dict[str, IntakeQuestionResponse] = {}
    for field in fields.values():
        if field.status in {FieldStatus.UNKNOWN, FieldStatus.REQUESTED}:
            question_id = f"Q-{field.field_id.replace('.', '-').upper()}"
            questions[question_id] = IntakeQuestionResponse(
                question_id,
                field.field_id,
                f"Provide {field.label.lower()}.",
                field.stakeholder,
                status=field.status,
            )
    return questions


def open_questions_for(intake: ProjectIntake) -> list[IntakeQuestionResponse]:
    return [
        question
        for question in intake.questions.values()
        if question.status in {FieldStatus.UNKNOWN, FieldStatus.REQUESTED} or not question.response
    ]


def _has_source_for_field(intake: ProjectIntake, field_id: str) -> bool:
    for source in intake.source_records.values():
        if field_id in source.field_ids:
            return True

    known_source_ids = set(intake.source_records)
    for question in intake.questions.values():
        if question.field_id == field_id and known_source_ids.intersection(question.source_ids):
            return True
    return False


def validate_intake(intake: ProjectIntake) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    required = required_fields_for(intake.deliverables)

    for field_id, requirement in required.items():
        actual = intake.fields.get(field_id, requirement)
        if actual.status in {FieldStatus.UNKNOWN, FieldStatus.REQUESTED} or not actual.value:
            findings.append(
                ValidationFinding(
                    "WARNING",
                    field_id,
                    f"{requirement.label} is missing for selected deliverables.",
                    ask=requirement.stakeholder,
                )
            )
        elif actual.status in {FieldStatus.ASSUMED, FieldStatus.ESTIMATED}:
            findings.append(
                ValidationFinding(
                    "WARNING",
                    field_id,
                    f"{requirement.label} is {actual.status.value.lower()} and needs verification.",
                    ask=requirement.stakeholder,
                )
            )
        elif actual.status in {FieldStatus.REJECTED, FieldStatus.SUPERSEDED}:
            findings.append(
                ValidationFinding(
                    "ERROR",
                    field_id,
                    f"{requirement.label} uses a {actual.status.value.lower()} value.",
                    ask=requirement.stakeholder,
                )
            )
        elif actual.status in {FieldStatus.VERIFIED, FieldStatus.APPROVED} and not _has_source_for_field(intake, field_id):
            findings.append(
                ValidationFinding(
                    "WARNING",
                    field_id,
                    f"{requirement.label} is {actual.status.value.lower()} but has no source record.",
                    ask=requirement.stakeholder,
                )
            )

    if not findings:
        findings.append(ValidationFinding("INFO", "intake", "No intake validation messages."))
    return findings

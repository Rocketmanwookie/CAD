# SPDX-License-Identifier: MIT
"""Missing-data matrix helpers for controls project intake."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from io import StringIO
from typing import Any

from controls_wb.intake import (
    Contact,
    FieldStatus,
    IntakeField,
    IntakeQuestionResponse,
    ProjectIntake,
    SourceRecord,
    SourceRecordType,
    required_fields_for,
)

MISSING_DATA_HEADERS = (
    "ItemId",
    "Category",
    "QuestionId",
    "FactId",
    "Label",
    "Required",
    "Value",
    "HasResponse",
    "SourceRecordIds",
    "SourceCount",
    "Verified",
    "Approved",
    "Status",
    "Severity",
    "Finding",
    "NextAction",
)


@dataclass(frozen=True)
class MissingDataRow:
    item_id: str
    category: str
    question_id: str
    fact_id: str
    label: str
    required: bool
    value: str
    has_response: bool
    source_record_ids: tuple[str, ...]
    source_count: int
    verified: bool
    approved: bool
    status: str
    severity: str
    finding: str
    next_action: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_record_ids"] = list(self.source_record_ids)
        return payload

    def to_csv_row(self) -> dict[str, Any]:
        return {
            "ItemId": self.item_id,
            "Category": self.category,
            "QuestionId": self.question_id,
            "FactId": self.fact_id,
            "Label": self.label,
            "Required": self.required,
            "Value": self.value,
            "HasResponse": self.has_response,
            "SourceRecordIds": ";".join(self.source_record_ids),
            "SourceCount": self.source_count,
            "Verified": self.verified,
            "Approved": self.approved,
            "Status": self.status,
            "Severity": self.severity,
            "Finding": self.finding,
            "NextAction": self.next_action,
        }


def _status(value: str) -> FieldStatus:
    try:
        return FieldStatus(value)
    except ValueError:
        return FieldStatus.UNKNOWN


def _status_for_value(value: str, status_value: str) -> FieldStatus:
    status = _status(status_value)
    if value and status in {FieldStatus.UNKNOWN, FieldStatus.REQUESTED}:
        return FieldStatus.RECEIVED
    return status


def _json_records(obj: object, attribute: str) -> list[dict[str, Any]]:
    records = []
    for item in getattr(obj, attribute, []) or []:
        try:
            record = json.loads(item)
        except (TypeError, ValueError):
            continue
        if isinstance(record, dict):
            records.append(record)
    return records


def _contacts_from_project_object(obj: object) -> dict[str, Contact]:
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


def _sources_from_project_object(obj: object) -> dict[str, SourceRecord]:
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


def _questions_from_project_object(obj: object) -> dict[str, IntakeQuestionResponse]:
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


def project_object_to_intake(obj: object) -> ProjectIntake:
    fields = {
        "project.name": IntakeField(
            "project.name",
            "Project name",
            "Project manager",
            value=getattr(obj, "ProjectName", ""),
            status=FieldStatus.RECEIVED if getattr(obj, "ProjectName", "") else FieldStatus.UNKNOWN,
        ),
        "project.customer": IntakeField(
            "project.customer",
            "Customer",
            "Project manager",
            value=getattr(obj, "Customer", ""),
            status=FieldStatus.RECEIVED if getattr(obj, "Customer", "") else FieldStatus.UNKNOWN,
        ),
        "project.siteLocation": IntakeField(
            "project.siteLocation",
            "Site/location",
            "Project manager",
            value=getattr(obj, "SiteLocation", ""),
            status=FieldStatus.RECEIVED if getattr(obj, "SiteLocation", "") else FieldStatus.UNKNOWN,
        ),
        "powerFeed.nominalVoltage": IntakeField(
            "powerFeed.nominalVoltage",
            "Nominal voltage",
            "Electrical engineering",
            value=getattr(obj, "NominalVoltage", ""),
            status=_status_for_value(
                getattr(obj, "NominalVoltage", ""),
                getattr(obj, "PowerFeedStatus", ""),
            ),
        ),
        "powerFeed.phaseCount": IntakeField(
            "powerFeed.phaseCount",
            "Phase count",
            "Electrical engineering",
            value=getattr(obj, "PhaseCount", ""),
            status=_status_for_value(
                getattr(obj, "PhaseCount", ""),
                getattr(obj, "PowerFeedStatus", ""),
            ),
        ),
        "environment.enclosureRating": IntakeField(
            "environment.enclosureRating",
            "Enclosure rating",
            "Operations / maintenance",
            value=getattr(obj, "EnclosureRating", ""),
            status=_status_for_value(
                getattr(obj, "EnclosureRating", ""),
                getattr(obj, "EnclosureRatingStatus", ""),
            ),
        ),
        "controls.plcPlatform": IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value=getattr(obj, "PlcPlatform", ""),
            status=_status_for_value(
                getattr(obj, "PlcPlatform", ""),
                getattr(obj, "PlcPlatformStatus", ""),
            ),
        ),
        "io.sensorCount": IntakeField(
            "io.sensorCount",
            "Sensor count or estimate",
            "Mechanical / materials handling",
            value=getattr(obj, "SensorCount", ""),
            status=_status_for_value(
                getattr(obj, "SensorCount", ""),
                getattr(obj, "SensorCountStatus", ""),
            ),
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


def _source_record_ids_for_field(intake: ProjectIntake, field_id: str) -> tuple[str, ...]:
    source_ids = {
        source.source_id
        for source in intake.source_records.values()
        if field_id in source.field_ids
    }
    known_source_ids = set(intake.source_records)
    for question in intake.questions.values():
        if question.field_id == field_id:
            source_ids.update(known_source_ids.intersection(question.source_ids))
    return tuple(sorted(source_ids))


def _question_for_field(intake: ProjectIntake, field_id: str) -> IntakeQuestionResponse | None:
    for question in intake.questions.values():
        if question.field_id == field_id:
            return question
    return None


def _category_for_field(field_id: str) -> str:
    return field_id.split(".", 1)[0] if "." in field_id else "intake"


def _classify_row(
    requirement: IntakeField,
    actual: IntakeField,
    question: IntakeQuestionResponse | None,
    source_record_ids: tuple[str, ...],
) -> tuple[str, str, str, str]:
    label = requirement.label
    owner = requirement.stakeholder
    value = actual.value or (question.response if question else "")
    has_response = bool(value)

    if not has_response or actual.status in {FieldStatus.UNKNOWN, FieldStatus.REQUESTED}:
        return (
            "missing_response",
            "error",
            f"{label} is required for selected deliverables and has no response.",
            f"Ask {owner} to provide {label.lower()}.",
        )
    if not source_record_ids:
        return (
            "missing_source",
            "warning",
            f"{label} has a response but no source record.",
            f"Attach or record a source for {label.lower()}.",
        )
    if actual.status == FieldStatus.APPROVED:
        return ("complete", "info", f"{label} is approved and source-backed.", "No action required.")
    if actual.status == FieldStatus.VERIFIED:
        return (
            "needs_approval",
            "warning",
            f"{label} is verified but not approved.",
            f"Route {label.lower()} to the responsible approver.",
        )
    if actual.status in {FieldStatus.REJECTED, FieldStatus.SUPERSEDED}:
        return (
            "missing_response",
            "error",
            f"{label} uses a {actual.status.value.lower()} response.",
            f"Ask {owner} for a current replacement response.",
        )
    return (
        "needs_verification",
        "warning",
        f"{label} has a response that still needs verification.",
        f"Verify {label.lower()} with {owner}.",
    )


def missing_data_matrix(project: ProjectIntake | object) -> list[MissingDataRow]:
    intake = project if isinstance(project, ProjectIntake) else project_object_to_intake(project)
    rows: list[MissingDataRow] = []

    for field_id, requirement in required_fields_for(intake.deliverables).items():
        actual = intake.fields.get(field_id, requirement)
        question = _question_for_field(intake, field_id)
        source_record_ids = _source_record_ids_for_field(intake, field_id)
        status, severity, finding, next_action = _classify_row(
            requirement,
            actual,
            question,
            source_record_ids,
        )
        value = actual.value or (question.response if question else "")
        rows.append(
            MissingDataRow(
                item_id=f"MD-{field_id.replace('.', '-').upper()}",
                category=_category_for_field(field_id),
                question_id=question.question_id if question else "",
                fact_id=field_id,
                label=requirement.label,
                required=True,
                value=value,
                has_response=bool(value),
                source_record_ids=source_record_ids,
                source_count=len(source_record_ids),
                verified=actual.status in {FieldStatus.VERIFIED, FieldStatus.APPROVED},
                approved=actual.status == FieldStatus.APPROVED,
                status=status,
                severity=severity,
                finding=finding,
                next_action=next_action,
            )
        )

    return rows


def missing_data_csv(rows: list[MissingDataRow]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=list(MISSING_DATA_HEADERS), lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row.to_csv_row())
    return output.getvalue()

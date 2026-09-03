# SPDX-License-Identifier: MIT
"""Missing-data matrix helpers for controls project intake."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from io import StringIO
from typing import Any

from controls_wb.fact_ids import FACT_SPECS, FactIds, category_for_fact_id, fact_spec, missing_data_item_id_for_fact_id
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


def _text_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def _line_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return "\n".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def _count_text(value: object) -> str:
    try:
        count = int(str(value).strip() or "0")
    except (TypeError, ValueError):
        return ""
    return str(max(count, 0)) if count else ""


def _sensor_count_value(obj: object) -> str:
    sensor_count = _count_text(getattr(obj, "SensorCount", ""))
    if sensor_count:
        return sensor_count
    di_count = _count_text(getattr(obj, "DICount", ""))
    ai_count = _count_text(getattr(obj, "AICount", ""))
    total = int(di_count or "0") + int(ai_count or "0")
    return str(total) if total else ""


def _enclosure_rating_value(obj: object) -> str:
    rating = _text_value(getattr(obj, "EnclosureRating", ""))
    if rating:
        return rating
    return _text_value(getattr(obj, "EnclosureRatings", ""))


def _field_status(obj: object, fact_id: str, value: str) -> FieldStatus:
    status_by_fact_id = {
        FactIds.POWER_NOMINAL_VOLTAGE: getattr(obj, "PowerFeedStatus", ""),
        FactIds.POWER_PHASE_COUNT: getattr(obj, "PowerFeedStatus", ""),
        FactIds.POWER_CONFIGURATION: getattr(obj, "PowerFeedStatus", ""),
        FactIds.ENCLOSURE_RATING: getattr(obj, "EnclosureRatingStatus", ""),
        FactIds.ENCLOSURE_RATINGS: getattr(obj, "EnclosureRatingStatus", ""),
        FactIds.PLC_PLATFORM: getattr(obj, "PlcPlatformStatus", ""),
        FactIds.SENSOR_COUNT: getattr(obj, "SensorCountStatus", ""),
        FactIds.DI_COUNT: getattr(obj, "SensorCountStatus", ""),
        FactIds.AI_COUNT: getattr(obj, "SensorCountStatus", ""),
    }
    return _status_for_value(value, status_by_fact_id.get(fact_id, ""))


def _project_fact_value(obj: object, property_name: str, fact_id: str) -> str:
    if fact_id == FactIds.SENSOR_COUNT:
        return _sensor_count_value(obj)
    if fact_id == FactIds.ENCLOSURE_RATING:
        return _enclosure_rating_value(obj)
    if fact_id == FactIds.CONTROLLED_LOADS:
        return _line_value(getattr(obj, property_name, ""))
    return _text_value(getattr(obj, property_name, ""))


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
    fields = {}
    for spec in FACT_SPECS:
        if not spec.property_name:
            continue
        value = _project_fact_value(obj, spec.property_name, spec.fact_id)
        fields[spec.fact_id] = IntakeField(
            field_id=spec.fact_id,
            label=spec.label,
            stakeholder=spec.stakeholder,
            value=value,
            status=_field_status(obj, spec.fact_id, value),
        )
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
                item_id=missing_data_item_id_for_fact_id(field_id),
                category=category_for_fact_id(field_id),
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

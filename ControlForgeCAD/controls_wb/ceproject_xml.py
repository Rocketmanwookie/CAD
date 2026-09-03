# SPDX-License-Identifier: MIT
"""Pure-Python CEProject XML import/export helpers."""

from __future__ import annotations

from dataclasses import dataclass
from xml.etree import ElementTree as ET

from controls_wb.intake import (
    Contact,
    FieldStatus,
    IntakeField,
    IntakeQuestionResponse,
    ProjectIntake,
    SourceRecord,
    SourceRecordType,
    ValidationFinding,
    validate_intake,
)
from controls_wb.missing_data import MissingDataRow, missing_data_matrix, project_object_to_intake


CEPROJECT_NAMESPACE = "https://whrsdaparty.github.io/ceproject/0.1"
ET.register_namespace("", CEPROJECT_NAMESPACE)


class CEProjectXmlError(ValueError):
    """Raised when a CEProject XML document cannot be parsed safely."""


@dataclass(frozen=True)
class CEProjectXmlValidationFinding:
    """Validation finding as it appears in CEProject XML."""

    finding_id: str
    level: str
    field_id: str
    message: str
    ask: str = ""


@dataclass(frozen=True)
class CEProjectXmlDocument:
    """Parsed CEProject XML content supported by the current intake model."""

    intake: ProjectIntake
    validation_findings: tuple[CEProjectXmlValidationFinding, ...] = ()
    missing_data_rows: tuple[MissingDataRow, ...] = ()


def _element(name: str, attrib: dict[str, str] | None = None) -> ET.Element:
    return ET.Element(f"{{{CEPROJECT_NAMESPACE}}}{name}", attrib or {})


def _child(parent: ET.Element, name: str, attrib: dict[str, str] | None = None) -> ET.Element:
    return ET.SubElement(parent, f"{{{CEPROJECT_NAMESPACE}}}{name}", attrib or {})


def _text_child(parent: ET.Element, name: str, text: str) -> ET.Element:
    child = _child(parent, name)
    child.text = text
    return child


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _intake(project: ProjectIntake | object) -> ProjectIntake:
    return project if isinstance(project, ProjectIntake) else project_object_to_intake(project)


def ceproject_element(project: ProjectIntake | object) -> ET.Element:
    """Build a deterministic CEProject XML element for an intake project."""
    intake = _intake(project)
    root = _element(
        "CEProject",
        {
            "schemaVersion": intake.schema_version,
            "projectId": intake.project_id,
        },
    )

    metadata = _child(root, "Metadata")
    _text_child(metadata, "Name", intake.name)

    _append_contacts(root, intake)
    _append_intake(root, intake)
    _append_source_records(root, intake)
    _append_validation_findings(root, intake)
    _append_missing_data_matrix(root, intake)
    return root


def ceproject_to_xml(project: ProjectIntake | object) -> str:
    """Serialize a project intake to deterministic CEProject XML text."""
    root = ceproject_element(project)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    return ET.tostring(root, encoding="unicode", xml_declaration=True, short_empty_elements=True)


def parse_ceproject_xml(xml_text: str | bytes) -> CEProjectXmlDocument:
    """Parse supported CEProject XML into a stable pure-Python representation."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise CEProjectXmlError(f"Invalid CEProject XML: {exc}") from exc

    _require_tag(root, "CEProject")
    project_id = _required_attr(root, "projectId", "CEProject")
    schema_version = _required_attr(root, "schemaVersion", "CEProject")
    metadata = _required_child(root, "Metadata", "CEProject")
    name = _required_text(metadata, "Name", "Metadata")

    intake = ProjectIntake(
        project_id=project_id,
        name=name,
        schema_version=schema_version,
        deliverables=_parse_deliverables(_child_or_none(root, "Intake")),
        fields=_parse_fields(_child_or_none(root, "Intake")),
        contacts=_parse_contacts(root),
        source_records=_parse_source_records(root),
        questions=_parse_questions(_child_or_none(root, "Intake")),
    )
    return CEProjectXmlDocument(
        intake=intake,
        validation_findings=_parse_validation_findings(root),
        missing_data_rows=_parse_missing_data_rows(root),
    )


def _append_contacts(root: ET.Element, intake: ProjectIntake) -> None:
    if not intake.contacts:
        return
    contacts = _child(root, "Contacts")
    for contact_id in sorted(intake.contacts):
        contact = intake.contacts[contact_id]
        _child(
            contacts,
            "Contact",
            {
                "contactId": contact.contact_id,
                "role": contact.role,
                "name": contact.name,
                "email": contact.email,
                "organization": contact.organization,
            },
        )


def _append_intake(root: ET.Element, intake: ProjectIntake) -> None:
    intake_element = _child(root, "Intake")
    if intake.deliverables:
        deliverables = _child(intake_element, "Deliverables")
        for deliverable in sorted(intake.deliverables):
            _child(deliverables, "Deliverable", {"id": deliverable})
    if intake.fields:
        fields = _child(intake_element, "Fields")
        for field_id in sorted(intake.fields):
            field = intake.fields[field_id]
            _child(
                fields,
                "Field",
                {
                    "fieldId": field.field_id,
                    "label": field.label,
                    "stakeholder": field.stakeholder,
                    "status": field.status.value,
                    "value": field.value,
                },
            )
    if intake.questions:
        questions = _child(intake_element, "Questions")
        for question_id in sorted(intake.questions):
            question = intake.questions[question_id]
            question_element = _child(
                questions,
                "Question",
                {
                    "questionId": question.question_id,
                    "fieldId": question.field_id,
                    "ask": question.ask,
                    "status": question.status.value,
                },
            )
            _text_child(question_element, "Prompt", question.prompt)
            if question.response:
                _text_child(question_element, "Response", question.response)
            if question.source_ids:
                source_refs = _child(question_element, "SourceRefs")
                for source_id in sorted(question.source_ids):
                    _child(source_refs, "SourceRef", {"sourceId": source_id})


def _append_source_records(root: ET.Element, intake: ProjectIntake) -> None:
    if not intake.source_records:
        return
    sources = _child(root, "SourceRecords")
    for source_id in sorted(intake.source_records):
        source = intake.source_records[source_id]
        source_element = _child(
            sources,
            "SourceRecord",
            {
                "sourceId": source.source_id,
                "type": source.source_type.value,
                "title": source.title,
                "stakeholder": source.stakeholder,
                "reference": source.reference,
                "receivedOn": source.received_on,
            },
        )
        if source.field_ids:
            field_refs = _child(source_element, "FieldRefs")
            for field_id in sorted(source.field_ids):
                _child(field_refs, "FieldRef", {"fieldId": field_id})


def _append_validation_findings(root: ET.Element, intake: ProjectIntake) -> None:
    findings = validate_intake(intake)
    if not findings:
        return
    validation = _child(root, "ValidationFindings")
    for index, finding in enumerate(findings, start=1):
        _child(
            validation,
            "Finding",
            {
                "findingId": f"VF-{index:03d}",
                "level": finding.level,
                "fieldId": finding.field_id,
                "ask": finding.ask,
                "message": finding.message,
            },
        )


def _append_missing_data_matrix(root: ET.Element, intake: ProjectIntake) -> None:
    rows = missing_data_matrix(intake)
    if not rows:
        return
    matrix = _child(root, "MissingDataMatrix")
    for row in sorted(rows, key=lambda item: item.item_id):
        row_element = _child(
            matrix,
            "MissingDataRow",
            {
                "itemId": row.item_id,
                "category": row.category,
                "questionId": row.question_id,
                "factId": row.fact_id,
                "label": row.label,
                "required": _bool(row.required),
                "value": row.value,
                "hasResponse": _bool(row.has_response),
                "sourceCount": str(row.source_count),
                "verified": _bool(row.verified),
                "approved": _bool(row.approved),
                "status": row.status,
                "severity": row.severity,
            },
        )
        _text_child(row_element, "Finding", row.finding)
        _text_child(row_element, "NextAction", row.next_action)
        if row.source_record_ids:
            source_refs = _child(row_element, "SourceRefs")
            for source_id in row.source_record_ids:
                _child(source_refs, "SourceRef", {"sourceId": source_id})


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[1] if element.tag.startswith("{") else element.tag


def _children(parent: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in list(parent) if _local_name(child) == name]


def _child_or_none(parent: ET.Element, name: str) -> ET.Element | None:
    matches = _children(parent, name)
    return matches[0] if matches else None


def _require_tag(element: ET.Element, name: str) -> None:
    if _local_name(element) != name:
        raise CEProjectXmlError(f"Expected root element {name}, found {_local_name(element)}.")


def _required_child(parent: ET.Element, name: str, context: str) -> ET.Element:
    child = _child_or_none(parent, name)
    if child is None:
        raise CEProjectXmlError(f"Missing required {name} element in {context}.")
    return child


def _required_text(parent: ET.Element, name: str, context: str) -> str:
    child = _required_child(parent, name, context)
    text = child.text or ""
    if not text:
        raise CEProjectXmlError(f"Missing required text for {context}/{name}.")
    return text


def _required_attr(element: ET.Element, attr: str, context: str) -> str:
    value = element.attrib.get(attr, "")
    if not value:
        raise CEProjectXmlError(f"Missing required {attr} attribute on {context}.")
    return value


def _status(value: str, context: str) -> FieldStatus:
    try:
        return FieldStatus(value)
    except ValueError as exc:
        raise CEProjectXmlError(f"Invalid field status {value!r} in {context}.") from exc


def _source_type(value: str, context: str) -> SourceRecordType:
    try:
        return SourceRecordType(value)
    except ValueError as exc:
        raise CEProjectXmlError(f"Invalid source record type {value!r} in {context}.") from exc


def _bool_attr(element: ET.Element, attr: str, context: str) -> bool:
    value = _required_attr(element, attr, context)
    if value == "true":
        return True
    if value == "false":
        return False
    raise CEProjectXmlError(f"Invalid boolean value {value!r} for {context}@{attr}.")


def _int_attr(element: ET.Element, attr: str, context: str) -> int:
    value = _required_attr(element, attr, context)
    try:
        return int(value)
    except ValueError as exc:
        raise CEProjectXmlError(f"Invalid integer value {value!r} for {context}@{attr}.") from exc


def _parse_deliverables(intake_element: ET.Element | None) -> set[str]:
    if intake_element is None:
        return set()
    deliverables = _child_or_none(intake_element, "Deliverables")
    if deliverables is None:
        return set()
    return {
        _required_attr(deliverable, "id", "Deliverable")
        for deliverable in _children(deliverables, "Deliverable")
    }


def _parse_fields(intake_element: ET.Element | None) -> dict[str, IntakeField]:
    if intake_element is None:
        return {}
    fields = _child_or_none(intake_element, "Fields")
    if fields is None:
        return {}
    parsed = {}
    for field in _children(fields, "Field"):
        field_id = _required_attr(field, "fieldId", "Field")
        parsed[field_id] = IntakeField(
            field_id=field_id,
            label=field.attrib.get("label", field_id),
            stakeholder=field.attrib.get("stakeholder", ""),
            status=_status(field.attrib.get("status", FieldStatus.UNKNOWN.value), f"Field {field_id}"),
            value=field.attrib.get("value", ""),
        )
    return parsed


def _parse_contacts(root: ET.Element) -> dict[str, Contact]:
    contacts = _child_or_none(root, "Contacts")
    if contacts is None:
        return {}
    parsed = {}
    for contact in _children(contacts, "Contact"):
        contact_id = _required_attr(contact, "contactId", "Contact")
        parsed[contact_id] = Contact(
            contact_id=contact_id,
            role=_required_attr(contact, "role", f"Contact {contact_id}"),
            name=contact.attrib.get("name", ""),
            email=contact.attrib.get("email", ""),
            organization=contact.attrib.get("organization", ""),
        )
    return parsed


def _parse_questions(intake_element: ET.Element | None) -> dict[str, IntakeQuestionResponse]:
    if intake_element is None:
        return {}
    questions = _child_or_none(intake_element, "Questions")
    if questions is None:
        return {}
    parsed = {}
    for question in _children(questions, "Question"):
        question_id = _required_attr(question, "questionId", "Question")
        source_refs = _child_or_none(question, "SourceRefs")
        parsed[question_id] = IntakeQuestionResponse(
            question_id=question_id,
            field_id=_required_attr(question, "fieldId", f"Question {question_id}"),
            prompt=_required_text(question, "Prompt", f"Question {question_id}"),
            ask=question.attrib.get("ask", ""),
            status=_status(
                question.attrib.get("status", FieldStatus.UNKNOWN.value),
                f"Question {question_id}",
            ),
            response=(_child_or_none(question, "Response").text or "") if _child_or_none(question, "Response") is not None else "",
            source_ids=tuple(
                _required_attr(source_ref, "sourceId", f"Question {question_id} SourceRef")
                for source_ref in _children(source_refs, "SourceRef")
            )
            if source_refs is not None
            else (),
        )
    return parsed


def _parse_source_records(root: ET.Element) -> dict[str, SourceRecord]:
    sources = _child_or_none(root, "SourceRecords")
    if sources is None:
        return {}
    parsed = {}
    for source in _children(sources, "SourceRecord"):
        source_id = _required_attr(source, "sourceId", "SourceRecord")
        field_refs = _child_or_none(source, "FieldRefs")
        parsed[source_id] = SourceRecord(
            source_id=source_id,
            source_type=_source_type(
                _required_attr(source, "type", f"SourceRecord {source_id}"),
                f"SourceRecord {source_id}",
            ),
            title=source.attrib.get("title", ""),
            stakeholder=source.attrib.get("stakeholder", ""),
            field_ids=tuple(
                _required_attr(field_ref, "fieldId", f"SourceRecord {source_id} FieldRef")
                for field_ref in _children(field_refs, "FieldRef")
            )
            if field_refs is not None
            else (),
            reference=source.attrib.get("reference", ""),
            received_on=source.attrib.get("receivedOn", ""),
        )
    return parsed


def _parse_validation_findings(root: ET.Element) -> tuple[CEProjectXmlValidationFinding, ...]:
    validation = _child_or_none(root, "ValidationFindings")
    if validation is None:
        return ()
    return tuple(
        CEProjectXmlValidationFinding(
            finding_id=_required_attr(finding, "findingId", "Finding"),
            level=_required_attr(finding, "level", "Finding"),
            field_id=_required_attr(finding, "fieldId", "Finding"),
            message=_required_attr(finding, "message", "Finding"),
            ask=finding.attrib.get("ask", ""),
        )
        for finding in _children(validation, "Finding")
    )


def _parse_missing_data_rows(root: ET.Element) -> tuple[MissingDataRow, ...]:
    matrix = _child_or_none(root, "MissingDataMatrix")
    if matrix is None:
        return ()
    rows = []
    for row in _children(matrix, "MissingDataRow"):
        item_id = _required_attr(row, "itemId", "MissingDataRow")
        source_refs = _child_or_none(row, "SourceRefs")
        rows.append(
            MissingDataRow(
                item_id=item_id,
                category=_required_attr(row, "category", f"MissingDataRow {item_id}"),
                question_id=row.attrib.get("questionId", ""),
                fact_id=_required_attr(row, "factId", f"MissingDataRow {item_id}"),
                label=_required_attr(row, "label", f"MissingDataRow {item_id}"),
                required=_bool_attr(row, "required", f"MissingDataRow {item_id}"),
                value=row.attrib.get("value", ""),
                has_response=_bool_attr(row, "hasResponse", f"MissingDataRow {item_id}"),
                source_record_ids=tuple(
                    _required_attr(source_ref, "sourceId", f"MissingDataRow {item_id} SourceRef")
                    for source_ref in _children(source_refs, "SourceRef")
                )
                if source_refs is not None
                else (),
                source_count=_int_attr(row, "sourceCount", f"MissingDataRow {item_id}"),
                verified=_bool_attr(row, "verified", f"MissingDataRow {item_id}"),
                approved=_bool_attr(row, "approved", f"MissingDataRow {item_id}"),
                status=_required_attr(row, "status", f"MissingDataRow {item_id}"),
                severity=_required_attr(row, "severity", f"MissingDataRow {item_id}"),
                finding=_required_text(row, "Finding", f"MissingDataRow {item_id}"),
                next_action=_required_text(row, "NextAction", f"MissingDataRow {item_id}"),
            )
        )
    return tuple(rows)

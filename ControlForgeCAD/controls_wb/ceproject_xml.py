# SPDX-License-Identifier: MIT
"""Pure-Python CEProject XML export helpers."""

from __future__ import annotations

from xml.etree import ElementTree as ET

from controls_wb.intake import ProjectIntake, validate_intake
from controls_wb.missing_data import missing_data_matrix, project_object_to_intake


CEPROJECT_NAMESPACE = "https://whrsdaparty.github.io/ceproject/0.1"
ET.register_namespace("", CEPROJECT_NAMESPACE)


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

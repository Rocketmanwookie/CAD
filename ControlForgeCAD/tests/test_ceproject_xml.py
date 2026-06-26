# SPDX-License-Identifier: MIT

from xml.etree import ElementTree as ET

from controls_wb.ceproject_xml import CEPROJECT_NAMESPACE, ceproject_to_xml
from controls_wb.intake import (
    Contact,
    FieldStatus,
    IntakeField,
    IntakeQuestionResponse,
    ProjectIntake,
    SourceRecord,
    SourceRecordType,
    default_project_intake,
)


NS = {"ce": CEPROJECT_NAMESPACE}


def _root(xml_text):
    return ET.fromstring(xml_text)


def test_ceproject_xml_exports_minimal_project():
    intake = ProjectIntake(project_id="CE-MIN", name="Minimal")

    xml_text = ceproject_to_xml(intake)
    root = _root(xml_text)

    assert xml_text == ceproject_to_xml(intake)
    assert root.tag == f"{{{CEPROJECT_NAMESPACE}}}CEProject"
    assert root.attrib == {"schemaVersion": "0.1.0", "projectId": "CE-MIN"}
    assert root.findtext("ce:Metadata/ce:Name", namespaces=NS) == "Minimal"
    assert root.find("ce:Intake", namespaces=NS) is not None


def test_ceproject_xml_exports_contacts_deterministically():
    intake = ProjectIntake(
        project_id="CE-CONTACTS",
        name="Contacts",
        contacts={
            "z_controls": Contact("z_controls", "Controls lead", "Zoe", "zoe@example.test", "Integrator"),
            "a_pm": Contact("a_pm", "Project manager", "Ada", "ada@example.test", "Customer"),
        },
    )

    root = _root(ceproject_to_xml(intake))
    contacts = root.findall("ce:Contacts/ce:Contact", namespaces=NS)

    assert [contact.attrib["contactId"] for contact in contacts] == ["a_pm", "z_controls"]
    assert contacts[0].attrib["email"] == "ada@example.test"


def test_ceproject_xml_exports_source_records_with_field_refs():
    intake = ProjectIntake(
        project_id="CE-SOURCES",
        name="Sources",
        source_records={
            "SRC-B": SourceRecord(
                "SRC-B",
                SourceRecordType.EMAIL,
                "Voltage confirmation",
                "Electrical engineering",
                field_ids=("powerFeed.phaseCount", "powerFeed.nominalVoltage"),
                reference="email:123",
                received_on="2026-06-26",
            ),
            "SRC-A": SourceRecord(
                "SRC-A",
                SourceRecordType.MANUAL_ENTRY,
                "Project setup",
                "Project manager",
                field_ids=("project.name",),
            ),
        },
    )

    root = _root(ceproject_to_xml(intake))
    sources = root.findall("ce:SourceRecords/ce:SourceRecord", namespaces=NS)
    field_refs = sources[1].findall("ce:FieldRefs/ce:FieldRef", namespaces=NS)

    assert [source.attrib["sourceId"] for source in sources] == ["SRC-A", "SRC-B"]
    assert sources[1].attrib["type"] == "email"
    assert [field.attrib["fieldId"] for field in field_refs] == [
        "powerFeed.nominalVoltage",
        "powerFeed.phaseCount",
    ]


def test_ceproject_xml_exports_intake_questions_and_responses():
    intake = ProjectIntake(
        project_id="CE-QUESTIONS",
        name="Questions",
        fields={
            "controls.plcPlatform": IntakeField(
                "controls.plcPlatform",
                "PLC platform",
                "Controls lead",
                value="Generic PLC",
                status=FieldStatus.RECEIVED,
            ),
        },
        questions={
            "Q-PLC": IntakeQuestionResponse(
                "Q-PLC",
                "controls.plcPlatform",
                "Provide PLC platform.",
                "Controls lead",
                status=FieldStatus.RECEIVED,
                response="Generic PLC",
                source_ids=("SRC-PLC",),
            )
        },
    )

    root = _root(ceproject_to_xml(intake))
    field = root.find("ce:Intake/ce:Fields/ce:Field", namespaces=NS)
    question = root.find("ce:Intake/ce:Questions/ce:Question", namespaces=NS)
    source_ref = question.find("ce:SourceRefs/ce:SourceRef", namespaces=NS)

    assert field.attrib["fieldId"] == "controls.plcPlatform"
    assert field.attrib["value"] == "Generic PLC"
    assert question.attrib["questionId"] == "Q-PLC"
    assert question.findtext("ce:Response", namespaces=NS) == "Generic PLC"
    assert source_ref.attrib["sourceId"] == "SRC-PLC"


def test_ceproject_xml_exports_validation_and_missing_data_findings():
    root = _root(ceproject_to_xml(default_project_intake()))

    findings = root.findall("ce:ValidationFindings/ce:Finding", namespaces=NS)
    rows = root.findall("ce:MissingDataMatrix/ce:MissingDataRow", namespaces=NS)

    assert any(
        finding.attrib["fieldId"] == "controls.plcPlatform"
        and finding.attrib["ask"] == "Controls lead"
        for finding in findings
    )
    assert any(
        row.attrib["factId"] == "controls.plcPlatform"
        and row.attrib["status"] == "missing_response"
        and row.attrib["severity"] == "error"
        for row in rows
    )

# SPDX-License-Identifier: MIT

import json
from types import SimpleNamespace

from controls_wb.intake import (
    FieldStatus,
    IntakeField,
    IntakeQuestionResponse,
    ProjectIntake,
    SourceRecord,
    SourceRecordType,
    default_project_intake,
)
from controls_wb.missing_data import missing_data_matrix, project_object_to_intake


def _source(field_id):
    return SourceRecord(
        f"SRC-{field_id.replace('.', '-').upper()}",
        SourceRecordType.EMAIL,
        "Stakeholder confirmation",
        "Controls lead",
        field_ids=(field_id,),
    )


def _intake_for(field, *, source=True):
    source_records = {_source(field.field_id).source_id: _source(field.field_id)} if source else {}
    return ProjectIntake(
        project_id="CE-DEMO",
        name="Demo",
        fields={
            "project.name": IntakeField(
                "project.name",
                "Project name",
                "Project manager",
                value="Demo",
                status=FieldStatus.APPROVED,
            ),
            field.field_id: field,
        },
        deliverables={"ioList"},
        source_records={
            "SRC-PROJECT": SourceRecord(
                "SRC-PROJECT",
                SourceRecordType.MANUAL_ENTRY,
                "Project setup",
                "Project manager",
                field_ids=("project.name",),
            ),
            **source_records,
        },
    )


def test_missing_data_matrix_marks_complete_when_approved_and_source_backed():
    intake = _intake_for(
        IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value="Generic PLC",
            status=FieldStatus.APPROVED,
        )
    )

    rows = {row.fact_id: row for row in missing_data_matrix(intake)}

    assert rows["controls.plcPlatform"].status == "complete"
    assert rows["controls.plcPlatform"].severity == "info"
    assert rows["controls.plcPlatform"].approved is True


def test_missing_data_matrix_marks_missing_response_for_requested_field():
    rows = {row.fact_id: row for row in missing_data_matrix(default_project_intake())}

    row = rows["controls.plcPlatform"]
    assert row.status == "missing_response"
    assert row.severity == "error"
    assert row.question_id == "Q-CONTROLS-PLCPLATFORM"
    assert row.next_action == "Ask Controls lead to provide plc platform."


def test_missing_data_matrix_marks_missing_source_for_unsourced_response():
    intake = _intake_for(
        IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value="Generic PLC",
            status=FieldStatus.APPROVED,
        ),
        source=False,
    )

    rows = {row.fact_id: row for row in missing_data_matrix(intake)}

    assert rows["controls.plcPlatform"].status == "missing_source"
    assert rows["controls.plcPlatform"].source_count == 0


def test_missing_data_matrix_marks_received_response_as_needs_verification():
    intake = _intake_for(
        IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value="Generic PLC",
            status=FieldStatus.RECEIVED,
        )
    )

    rows = {row.fact_id: row for row in missing_data_matrix(intake)}

    assert rows["controls.plcPlatform"].status == "needs_verification"
    assert rows["controls.plcPlatform"].verified is False


def test_missing_data_matrix_marks_verified_response_as_needs_approval():
    intake = _intake_for(
        IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value="Generic PLC",
            status=FieldStatus.VERIFIED,
        )
    )

    rows = {row.fact_id: row for row in missing_data_matrix(intake)}

    assert rows["controls.plcPlatform"].status == "needs_approval"
    assert rows["controls.plcPlatform"].verified is True
    assert rows["controls.plcPlatform"].approved is False


def test_missing_data_matrix_uses_question_response_sources_and_project_objects():
    source_record = {
        "id": "SRC-001",
        "type": "meeting_note",
        "title": "I/O review",
        "stakeholder": "Mechanical / materials handling",
    }
    question = IntakeQuestionResponse(
        "Q-SENSORS",
        "io.sensorCount",
        "Provide sensor count.",
        "Mechanical / materials handling",
        status=FieldStatus.RECEIVED,
        response="12",
        source_ids=("SRC-001",),
    )
    obj = SimpleNamespace(
        ProjectId="CE-PROJECT-001",
        ProjectName="Controls Project",
        SchemaVersion="0.1.0",
        Deliverables=["ioList"],
        PlcPlatform="Generic PLC",
        PlcPlatformStatus="Approved",
        SensorCount="",
        SensorCountStatus="Approved",
        SourceRecords=[
            json.dumps(
                {
                    "id": "SRC-PLC",
                    "type": "email",
                    "title": "PLC approval",
                    "stakeholder": "Controls lead",
                    "fieldIds": ["controls.plcPlatform"],
                }
            ),
            json.dumps(source_record),
        ],
        IntakeQuestions=[
            json.dumps(
                {
                    "id": question.question_id,
                    "fieldId": question.field_id,
                    "prompt": question.prompt,
                    "ask": question.ask,
                    "status": question.status.value,
                    "response": question.response,
                    "sourceIds": list(question.source_ids),
                }
            )
        ],
    )

    rows = {row.fact_id: row for row in missing_data_matrix(obj)}

    assert rows["controls.plcPlatform"].status == "complete"
    assert rows["io.sensorCount"].value == "12"
    assert rows["io.sensorCount"].source_record_ids == ("SRC-001",)
    assert rows["io.sensorCount"].status == "complete"


def test_project_object_to_intake_converts_editable_properties_to_backend_fields():
    obj = SimpleNamespace(
        ProjectId="CE-PROJECT-001",
        ProjectName="Line 7",
        Customer="Acme",
        SiteLocation="Cleveland",
        SchemaVersion="0.1.0",
        Deliverables=["ioList", "panelLayout"],
        NominalVoltage="480",
        PhaseCount="3",
        EnclosureRating="NEMA 12",
        PlcPlatform="Generic PLC",
        SensorCount="18",
        PowerFeedStatus="Requested",
        EnclosureRatingStatus="Requested",
        PlcPlatformStatus="Requested",
        SensorCountStatus="Requested",
    )

    intake = project_object_to_intake(obj)

    assert intake.fields["project.name"].value == "Line 7"
    assert intake.fields["project.customer"].value == "Acme"
    assert intake.fields["project.siteLocation"].value == "Cleveland"
    assert intake.fields["powerFeed.nominalVoltage"].status == FieldStatus.RECEIVED
    assert intake.fields["powerFeed.phaseCount"].status == FieldStatus.RECEIVED
    assert intake.fields["environment.enclosureRating"].status == FieldStatus.RECEIVED
    assert intake.fields["controls.plcPlatform"].status == FieldStatus.RECEIVED
    assert intake.fields["io.sensorCount"].status == FieldStatus.RECEIVED


def test_missing_data_matrix_recognizes_filled_editable_project_values():
    obj = SimpleNamespace(
        ProjectId="CE-PROJECT-001",
        ProjectName="Line 7",
        SchemaVersion="0.1.0",
        Deliverables=["ioList"],
        PlcPlatform="Generic PLC",
        SensorCount="12",
        PlcPlatformStatus="Requested",
        SensorCountStatus="Requested",
    )

    rows = {row.fact_id: row for row in missing_data_matrix(obj)}

    assert rows["controls.plcPlatform"].value == "Generic PLC"
    assert rows["controls.plcPlatform"].status == "missing_source"
    assert rows["io.sensorCount"].value == "12"
    assert rows["io.sensorCount"].status == "missing_source"

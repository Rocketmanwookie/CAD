# SPDX-License-Identifier: MIT

from controls_wb.intake import (
    FieldStatus,
    IntakeField,
    IntakeQuestionResponse,
    ProjectIntake,
    SourceRecord,
    SourceRecordType,
    default_project_intake,
    open_questions_for,
    required_fields_for,
    validate_intake,
)


def test_required_fields_are_merged_for_selected_deliverables():
    required = required_fields_for(["panelLayout", "ioList"])

    assert "project.name" in required
    assert "powerFeed.nominalVoltage" in required
    assert "controls.plcPlatform" in required


def test_default_project_intake_reports_missing_requested_fields_with_ask_owner():
    intake = default_project_intake()
    findings = validate_intake(intake)

    messages = [finding.message for finding in findings]
    asks = [finding.ask for finding in findings]
    assert any("Nominal voltage is missing" in message for message in messages)
    assert "Electrical engineering" in asks
    assert "Controls lead" in asks
    assert any(question.field_id == "controls.plcPlatform" for question in open_questions_for(intake))


def test_verified_required_intake_has_no_warnings():
    source = SourceRecord(
        "SRC-001",
        SourceRecordType.EMAIL,
        "Controls platform confirmation",
        "Controls lead",
        field_ids=("controls.plcPlatform", "io.sensorCount"),
    )
    fields = {
        "project.name": IntakeField(
            "project.name",
            "Project name",
            "Project manager",
            value="Demo",
            status=FieldStatus.RECEIVED,
        ),
        "controls.plcPlatform": IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value="Generic PLC",
            status=FieldStatus.VERIFIED,
        ),
        "io.sensorCount": IntakeField(
            "io.sensorCount",
            "Sensor count or estimate",
            "Mechanical / materials handling",
            value="12",
            status=FieldStatus.VERIFIED,
        ),
    }
    intake = ProjectIntake(
        project_id="CE-DEMO",
        name="Demo",
        fields=fields,
        deliverables={"ioList"},
        source_records={source.source_id: source},
    )

    findings = validate_intake(intake)

    assert [(finding.level, finding.message) for finding in findings] == [
        ("INFO", "No intake validation messages.")
    ]


def test_verified_required_intake_requires_source_record():
    fields = {
        "project.name": IntakeField(
            "project.name",
            "Project name",
            "Project manager",
            value="Demo",
            status=FieldStatus.RECEIVED,
        ),
        "controls.plcPlatform": IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value="Generic PLC",
            status=FieldStatus.VERIFIED,
        ),
        "io.sensorCount": IntakeField(
            "io.sensorCount",
            "Sensor count or estimate",
            "Mechanical / materials handling",
            value="12",
            status=FieldStatus.VERIFIED,
        ),
    }
    intake = ProjectIntake(project_id="CE-DEMO", name="Demo", fields=fields, deliverables={"ioList"})

    findings = validate_intake(intake)

    assert (
        "WARNING",
        "controls.plcPlatform",
        "PLC platform is verified but has no source record.",
        "Controls lead",
    ) in [(finding.level, finding.field_id, finding.message, finding.ask) for finding in findings]


def test_question_response_source_ids_satisfy_source_traceability():
    source = SourceRecord(
        "SRC-001",
        SourceRecordType.MEETING_NOTE,
        "I/O review",
        "Mechanical / materials handling",
    )
    fields = {
        "project.name": IntakeField(
            "project.name",
            "Project name",
            "Project manager",
            value="Demo",
            status=FieldStatus.RECEIVED,
        ),
        "controls.plcPlatform": IntakeField(
            "controls.plcPlatform",
            "PLC platform",
            "Controls lead",
            value="Generic PLC",
            status=FieldStatus.VERIFIED,
        ),
        "io.sensorCount": IntakeField(
            "io.sensorCount",
            "Sensor count or estimate",
            "Mechanical / materials handling",
            value="12",
            status=FieldStatus.VERIFIED,
        ),
    }
    questions = {
        "Q-PLC": IntakeQuestionResponse(
            "Q-PLC",
            "controls.plcPlatform",
            "Provide plc platform.",
            "Controls lead",
            status=FieldStatus.RECEIVED,
            response="Generic PLC",
            source_ids=("SRC-001",),
        ),
        "Q-SENSORS": IntakeQuestionResponse(
            "Q-SENSORS",
            "io.sensorCount",
            "Provide sensor count.",
            "Mechanical / materials handling",
            status=FieldStatus.RECEIVED,
            response="12",
            source_ids=("SRC-001",),
        ),
    }
    intake = ProjectIntake(
        project_id="CE-DEMO",
        name="Demo",
        fields=fields,
        deliverables={"ioList"},
        source_records={source.source_id: source},
        questions=questions,
    )

    findings = validate_intake(intake)

    assert [(finding.level, finding.message) for finding in findings] == [
        ("INFO", "No intake validation messages.")
    ]

# SPDX-License-Identifier: MIT

from controls_wb.intake import (
    FieldStatus,
    IntakeField,
    ProjectIntake,
    default_project_intake,
    required_fields_for,
    validate_intake,
)


def test_required_fields_are_merged_for_selected_deliverables():
    required = required_fields_for(["panelLayout", "ioList"])

    assert "project.name" in required
    assert "powerFeed.nominalVoltage" in required
    assert "controls.plcPlatform" in required


def test_default_project_intake_reports_missing_requested_fields_with_ask_owner():
    findings = validate_intake(default_project_intake())

    messages = [finding.message for finding in findings]
    asks = [finding.ask for finding in findings]
    assert any("Nominal voltage is missing" in message for message in messages)
    assert "Electrical engineering" in asks
    assert "Controls lead" in asks


def test_verified_required_intake_has_no_warnings():
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
    )

    findings = validate_intake(intake)

    assert [(finding.level, finding.message) for finding in findings] == [
        ("INFO", "No intake validation messages.")
    ]

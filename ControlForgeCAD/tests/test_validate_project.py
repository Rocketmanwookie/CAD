# SPDX-License-Identifier: MIT

from types import SimpleNamespace

from controls_wb.commands.validate_project import validate_document_objects


def test_validate_document_objects_reports_duplicate_tags():
    messages = validate_document_objects(
        [
            SimpleNamespace(Tag="M101", Description="Motor", PartNumber="PN-1"),
            SimpleNamespace(Tag="M101", Description="Motor duplicate", PartNumber="PN-2"),
        ]
    )

    assert ("ERROR", "Duplicate tag: M101") in messages


def test_validate_document_objects_reports_project_intake_owner():
    messages = validate_document_objects(
        [
            SimpleNamespace(
                ProjectId="CE-PROJECT-001",
                ProjectName="Controls Project",
                SchemaVersion="0.1.0",
                Deliverables=["ioList"],
                PlcPlatformStatus="Requested",
                SensorCountStatus="Requested",
            )
        ]
    )

    assert (
        "WARNING",
        "PLC platform is missing for selected deliverables. Ask: Controls lead.",
    ) in messages

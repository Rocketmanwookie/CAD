# SPDX-License-Identifier: MIT

import json
from types import SimpleNamespace

from controls_wb.commands.validate_project import validate_document_objects
from controls_wb.connections import SignalConnection, serialize_connection
from controls_wb.identity import new_ce_identity


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


def test_validate_document_objects_uses_project_source_records():
    messages = validate_document_objects(
        [
            SimpleNamespace(
                ProjectId="CE-PROJECT-001",
                ProjectName="Controls Project",
                SchemaVersion="0.1.0",
                Deliverables=["ioList"],
                PlcPlatform="Generic PLC",
                PlcPlatformStatus="Verified",
                SensorCount="12",
                SensorCountStatus="Verified",
                SourceRecords=[
                    json.dumps(
                        {
                            "id": "SRC-001",
                            "type": "email",
                            "title": "Controls confirmation",
                            "stakeholder": "Controls lead",
                            "fieldIds": ["controls.plcPlatform", "io.sensorCount"],
                        }
                    )
                ],
            )
        ]
    )

    assert messages == [("INFO", "No intake validation messages.")]


def test_validate_document_objects_reads_edited_project_properties():
    messages = validate_document_objects(
        [
            SimpleNamespace(
                ProjectId="CE-PROJECT-001",
                ProjectName="Controls Project",
                SchemaVersion="0.1.0",
                Deliverables=["ioList"],
                PlcPlatform="Generic PLC",
                SensorCount="12",
                PlcPlatformStatus="Requested",
                SensorCountStatus="Requested",
            )
        ]
    )

    assert (
        "WARNING",
        "PLC platform is missing for selected deliverables. Ask: Controls lead.",
    ) not in messages
    assert (
        "WARNING",
        "Sensor count or estimate is missing for selected deliverables. Ask: Mechanical / materials handling.",
    ) not in messages
    assert (
        "WARNING",
        "PLC platform has a response but no source record.",
    ) not in messages
    assert messages == [("INFO", "No intake validation messages.")]


def test_validate_document_objects_reports_blank_edited_project_property():
    messages = validate_document_objects(
        [
            SimpleNamespace(
                ProjectId="CE-PROJECT-001",
                ProjectName="Controls Project",
                SchemaVersion="0.1.0",
                Deliverables=["ioList"],
                PlcPlatform="Generic PLC",
                SensorCount="",
                PlcPlatformStatus="Requested",
                SensorCountStatus="Requested",
            )
        ]
    )

    assert (
        "WARNING",
        "Sensor count or estimate is missing for selected deliverables. Ask: Mechanical / materials handling.",
    ) in messages


def test_validate_document_objects_reports_broken_typed_electrical_graph():
    path = SimpleNamespace(
        CEIdentity=new_ce_identity(),
        SignalIdentity=new_ce_identity(),
        SignalObject=None,
        TerminalObjects=[],
        WireObjects=[],
    )
    project = SimpleNamespace(
        ProjectId="CE-PROJECT-001",
        ProjectName="Controls Project",
        SchemaVersion="0.1.0",
        Deliverables=[],
        ElectricalPaths=[path],
        ElectricalSignals=[],
        ElectricalDevices=[],
    )

    messages = validate_document_objects([project])

    assert any(
        level == "ERROR" and "Electrical graph could not be reconstructed" in message
        for level, message in messages
    )


def test_validate_document_objects_reports_dangling_connection_record_reference():
    connection = SignalConnection(
        "CONN-0001",
        "DI-0001",
        path_identity="missing-path",
        signal_identity="missing-signal",
        plc_device_identity="missing-plc",
        terminal_strip_identity="missing-strip",
        field_device_identity="missing-field",
        terminal_identities=("missing-terminal",),
        wire_identities=("missing-wire",),
    )
    project = SimpleNamespace(
        ProjectId="CE-PROJECT-001",
        ProjectName="Controls Project",
        SchemaVersion="0.1.0",
        Deliverables=[],
        ConnectionRecords=[serialize_connection(connection)],
    )

    messages = validate_document_objects([project])

    assert ("ERROR", "CONN-0001 has a dangling path identity missing-path.") in messages

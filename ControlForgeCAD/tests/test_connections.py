# SPDX-License-Identifier: MIT

from types import SimpleNamespace

from controls_wb.connections import (
    CONNECTION_SCHEDULE_HEADERS,
    SignalConnection,
    connection_findings,
    connection_schedule_csv,
    connections_from_project,
    deserialize_connection,
    serialize_connection,
)
from controls_wb.commands.export_connection_schedule import connection_schedule_csv_for_objects
from controls_wb.gui.connection import add_connection_from_form


def test_connection_round_trip_and_project_storage():
    connection = SignalConnection(
        connection_id="CONN-001",
        signal_tag="DI-0001",
        field_device="PE-101",
        terminal_strip="TB-001",
        terminal="1",
        wire_tag="W-1001",
        plc_rack="PLC-001",
        plc_slot="0",
        plc_channel="0",
        status="planned",
    )
    assert deserialize_connection(serialize_connection(connection)) == connection
    assert connections_from_project(SimpleNamespace(ConnectionRecords=[serialize_connection(connection)])) == [connection]


def test_connection_schedule_is_stable_and_traceable():
    connection = SignalConnection("CONN-001", "DI-0001", "PE-101", "TB-001", "1", "W-1001", "PLC-001", "0", "0")
    csv_text = connection_schedule_csv([connection])
    assert csv_text.splitlines()[0].split(",") == list(CONNECTION_SCHEDULE_HEADERS)
    assert "CONN-001,DI-0001,PE-101,TB-001,1,W-1001,PLC-001,0,0,planned" in csv_text


def test_connection_findings_cover_incomplete_and_duplicate_terminal_records():
    first = SignalConnection("CONN-001", "DI-0001", "PE-101", "TB-001", "1", "W-1001")
    duplicate = SignalConnection("CONN-002", "DI-0002", "LS-101", "TB-001", "1", "W-1002")
    incomplete = SignalConnection("CONN-003", "DI-0003")
    findings = connection_findings([first, duplicate, incomplete])
    assert "ERROR: CONN-002 and CONN-001 use TB-001:1." in findings
    assert "WARNING: CONN-003 is missing wire tag." in findings


def test_connection_form_persists_record_and_export_reads_project_objects():
    project = SimpleNamespace(ProjectId="CE-PROJECT-001", Deliverables=[], ConnectionRecords=[])
    document = SimpleNamespace(Objects=[project])
    connection = add_connection_from_form(
        document,
        {
            "signal_tag": "DI-0001",
            "field_device": "PE-101",
            "terminal_strip": "TB-001",
            "terminal": "1",
            "wire_tag": "W-1001",
            "plc_rack": "PLC-001",
            "plc_slot": "0",
            "plc_channel": "0",
        },
    )
    assert connection.connection_id == "CONN-0001"
    assert "CONN-0001,DI-0001,PE-101,TB-001,1,W-1001,PLC-001,0,0,planned" in connection_schedule_csv_for_objects([project])

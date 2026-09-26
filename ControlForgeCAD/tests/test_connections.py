# SPDX-License-Identifier: MIT

from dataclasses import replace
from types import SimpleNamespace

from controls_wb.connections import (
    CONNECTION_SCHEDULE_HEADERS,
    SignalConnection,
    append_connection_for_path,
    connection_findings,
    connection_reference_findings,
    connection_typed_path_findings,
    connection_schedule_csv,
    connections_from_project,
    deserialize_connection,
    serialize_connection,
)
from controls_wb.commands.export_connection_schedule import connection_schedule_csv_for_objects
from controls_wb.gui.connection import add_connection_from_form
from controls_wb.identity import CERoles


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


def test_manual_connection_record_cannot_duplicate_a_typed_path_signal():
    typed_path = SimpleNamespace(CEIdentity="path-id", SignalTag="DI-0001")
    project = SimpleNamespace(
        ProjectId="CE-PROJECT-001", Deliverables=[], ConnectionRecords=[], ElectricalPaths=[typed_path]
    )
    document = SimpleNamespace(Objects=[project])

    try:
        add_connection_from_form(document, {"signal_tag": "DI-0001"})
    except ValueError as exc:
        assert "already has a typed electrical path" in str(exc)
    else:
        raise AssertionError("manual record should not duplicate a typed electrical path")


def test_connection_validation_reports_legacy_record_that_duplicates_typed_path_signal():
    legacy = SignalConnection("CONN-0001", "DI-0001")
    typed_path = SimpleNamespace(CEIdentity="path-id", SignalTag="DI-0001")

    assert connection_typed_path_findings([legacy], [typed_path]) == [
        "ERROR: CONN-0001 duplicates typed electrical path data for signal DI-0001."
    ]


def _linked_objects():
    plc = SimpleNamespace(CEIdentity="plc-id", CERole=CERoles.PLC_CONTROLLER, Tag="PLC-001")
    strip = SimpleNamespace(CEIdentity="strip-id", CERole=CERoles.TERMINAL_STRIP, Tag="TB-001")
    field = SimpleNamespace(CEIdentity="field-id", CERole=CERoles.FIELD_DEVICE, Tag="PE-101")
    signal = SimpleNamespace(CEIdentity="signal-id", CERole=CERoles.SIGNAL, SignalTag="DI-0001")
    terminals = (
        SimpleNamespace(CEIdentity="terminal-plc", CERole=CERoles.PLC_CHANNEL_TERMINAL, OwnerIdentity=plc.CEIdentity, Designation="X1.0"),
        SimpleNamespace(CEIdentity="terminal-in", CERole=CERoles.CABINET_TERMINAL, OwnerIdentity=strip.CEIdentity, Designation="1-IN"),
        SimpleNamespace(CEIdentity="terminal-out", CERole=CERoles.CABINET_TERMINAL, OwnerIdentity=strip.CEIdentity, Designation="1-OUT"),
        SimpleNamespace(CEIdentity="terminal-field", CERole=CERoles.DEVICE_TERMINAL, OwnerIdentity=field.CEIdentity, Designation="1"),
    )
    wires = tuple(
        SimpleNamespace(CEIdentity=f"wire-{index}", CERole=CERoles.WIRE, WireTag=tag)
        for index, tag in enumerate(("W-001", "JMP-001", "W-002"), start=1)
    )
    path = SimpleNamespace(
        CEIdentity="path-id",
        CERole=CERoles.CONNECTION_PATH,
        SignalIdentity=signal.CEIdentity,
        SignalTag=signal.SignalTag,
        TerminalObjects=list(terminals),
        WireObjects=list(wires),
    )
    project = SimpleNamespace(ConnectionRecords=[], ElectricalDevices=[plc, strip, field])
    return project, path, signal, (plc, strip, field), terminals, wires


def test_materialized_path_bridge_persists_ordered_object_identities():
    project, path, signal, devices, terminals, wires = _linked_objects()

    connection = append_connection_for_path(project, path)

    assert connection.path_identity == path.CEIdentity
    assert connection.signal_identity == signal.CEIdentity
    assert connection.plc_device_identity == devices[0].CEIdentity
    assert connection.terminal_strip_identity == devices[1].CEIdentity
    assert connection.field_device_identity == devices[2].CEIdentity
    assert connection.terminal_identities == tuple(item.CEIdentity for item in terminals)
    assert connection.wire_identities == tuple(item.CEIdentity for item in wires)
    assert connections_from_project(project) == [connection]
    assert connection_reference_findings(
        [connection], [path, signal, *devices, *terminals, *wires]
    ) == []


def test_connection_reference_findings_cover_legacy_dangling_and_wrong_order():
    legacy = SignalConnection("CONN-0001", "DI-0001")
    assert connection_reference_findings([legacy], []) == [
        "WARNING: CONN-0001 is not linked to a typed electrical path."
    ]

    project, path, signal, devices, terminals, wires = _linked_objects()
    connection = append_connection_for_path(project, path)
    broken = replace(
        connection,
        field_device_identity="missing-device",
        terminal_identities=tuple(reversed(connection.terminal_identities)),
    )
    findings = connection_reference_findings(
        [broken], [path, signal, *devices, *terminals, *wires]
    )
    assert "ERROR: CONN-0001 has a dangling field device identity missing-device." in findings
    assert "ERROR: CONN-0001 terminal identities do not match its typed path order." in findings

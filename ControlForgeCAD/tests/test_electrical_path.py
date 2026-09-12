# SPDX-License-Identifier: MIT

from dataclasses import replace

import pytest

from controls_wb.electrical_path import (
    ElectricalConnectionPath,
    RoutePoint,
    TerminalEndpoint,
    WireSegment,
    deserialize_connection_path,
    io_schedule_row,
    serialize_connection_path,
    wiring_schedule_rows,
    connection_path_from_xml,
    connection_path_to_xml,
)
from controls_wb.identity import CERoles, new_ce_identity


def _path():
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, new_ce_identity(), "PLC1:X1.0")
    terminal_in = TerminalEndpoint(new_ce_identity(), CERoles.CABINET_TERMINAL, new_ce_identity(), "TB1:1-IN")
    terminal_out = TerminalEndpoint(
        new_ce_identity(), CERoles.CABINET_TERMINAL, terminal_in.owner_identity, "TB1:1-OUT"
    )
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, new_ce_identity(), "LS1:1")
    wires = (
        WireSegment(
            new_ce_identity(), plc.identity, terminal_in.identity, "W-001",
            route=(RoutePoint(0, 0, 0), RoutePoint(30, 40, 0)),
        ),
        WireSegment(new_ce_identity(), terminal_in.identity, terminal_out.identity, "JMP-001", specified_length_mm=5),
        WireSegment(
            new_ce_identity(), terminal_out.identity, device.identity, "W-002",
            route=(RoutePoint(30, 40, 0), RoutePoint(30, 40, 100)),
        ),
    )
    return ElectricalConnectionPath(
        new_ce_identity(), new_ce_identity(), "DI-0001", (plc, terminal_in, terminal_out, device), wires
    )


def test_connection_path_is_continuous_and_round_trips_deterministically():
    path = _path()

    serialized = serialize_connection_path(path)
    restored = deserialize_connection_path(serialized)

    assert restored == path
    assert serialize_connection_path(restored) == serialized
    assert path.total_length_mm == 155.0


def test_connection_path_xml_is_namespace_correct_schema_valid_and_deterministic():
    lxml = pytest.importorskip("lxml.etree")
    path = _path()
    xml_text = connection_path_to_xml(path)
    schema_path = __import__("pathlib").Path(__file__).resolve().parents[1] / "schemas" / "connection_path_v1.xsd"
    schema = lxml.XMLSchema(lxml.parse(str(schema_path)))

    schema.assertValid(lxml.fromstring(xml_text.encode("utf-8")))
    restored = connection_path_from_xml(xml_text)

    assert restored == path
    assert connection_path_to_xml(restored) == xml_text


def test_connection_path_xml_rejects_missing_namespace():
    xml_text = connection_path_to_xml(_path()).replace(
        "https://whrsdaparty.github.io/ceproject/connection-path/1.0",
        "https://example.invalid/not-ceproject",
    )

    with pytest.raises(ValueError, match="namespaced ConnectionPath"):
        connection_path_from_xml(xml_text)


def test_connection_path_rejects_a_wire_that_skips_ordered_terminal():
    path = _path()
    broken_wire = replace(path.wires[0], to_terminal_identity=path.terminals[2].identity)

    with pytest.raises(ValueError, match="does not end at ordered terminal"):
        replace(path, wires=(broken_wire,) + path.wires[1:]).validate()


def test_connection_path_requires_plc_to_device_direction():
    path = _path()

    with pytest.raises(ValueError, match="must start at a PLC"):
        replace(path, terminals=(replace(path.terminals[0], role=CERoles.CABINET_TERMINAL),) + path.terminals[1:]).validate()


def test_wiring_and_io_schedules_are_projections_of_same_path():
    path = _path()

    wiring = wiring_schedule_rows(path)
    io = io_schedule_row(path)

    assert [row["WireTag"] for row in wiring] == ["W-001", "JMP-001", "W-002"]
    assert [row["LengthMm"] for row in wiring] == [50.0, 5, 100.0]
    assert io["SignalIdentity"] == path.signal_identity
    assert io["TerminalPath"] == "PLC1:X1.0 > TB1:1-IN > TB1:1-OUT > LS1:1"
    assert io["TotalLengthMm"] == 155.0

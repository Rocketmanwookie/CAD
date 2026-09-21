# SPDX-License-Identifier: MIT

from dataclasses import replace

from controls_wb.electrical_path import ElectricalConnectionPath, TerminalEndpoint, WireSegment
from controls_wb.electrical_validation import validate_connection_graph
from controls_wb.identity import CERoles, new_ce_identity


def _complete_path():
    plc_owner = new_ce_identity()
    device_owner = new_ce_identity()
    signal = new_ce_identity()
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, plc_owner, "PLC1:X1.0")
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, device_owner, "LS1:1")
    wire = WireSegment(
        new_ce_identity(), plc.identity, device.identity, "W-001",
        conductor_size="18 AWG", color="blue", specified_length_mm=1000,
    )
    path = ElectricalConnectionPath(new_ce_identity(), signal, "DI-0001", (plc, device), (wire,))
    return path, {plc_owner, device_owner}, {signal}


def test_complete_graph_has_no_findings():
    path, owners, signals = _complete_path()

    assert validate_connection_graph((path,), known_owner_identities=owners, known_signal_identities=signals) == ()


def test_graph_reports_dangling_references_and_schedule_data():
    path, _, _ = _complete_path()
    incomplete_wire = replace(path.wires[0], conductor_size="", color="", specified_length_mm=None)

    findings = validate_connection_graph(
        (replace(path, wires=(incomplete_wire,)),),
        known_owner_identities=set(),
        known_signal_identities=set(),
    )
    codes = [finding.code for finding in findings]

    assert codes.count("dangling_terminal_owner") == 2
    assert "dangling_signal" in codes
    assert "missing_conductor_size" in codes
    assert "missing_wire_color" in codes
    assert "missing_wire_length" in codes


def test_graph_rejects_terminal_shared_between_different_signals():
    first, owners, signals = _complete_path()
    second_signal = new_ce_identity()
    second = replace(first, identity=new_ce_identity(), signal_identity=second_signal, signal_tag="DI-0002")

    findings = validate_connection_graph(
        (first, second),
        known_owner_identities=owners,
        known_signal_identities=signals | {second_signal},
    )

    assert any(finding.code == "terminal_signal_conflict" for finding in findings)
    assert any(finding.code == "duplicate_identity" and finding.identity == first.wires[0].identity for finding in findings)

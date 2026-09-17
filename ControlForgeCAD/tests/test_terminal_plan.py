# SPDX-License-Identifier: MIT

from controls_wb.electrical_path import ElectricalConnectionPath, TerminalEndpoint, WireSegment
from controls_wb.identity import CERoles, new_ce_identity
from controls_wb.terminal_plan import terminal_plan_csv, terminal_plan_rows


def _path():
    plc = TerminalEndpoint(new_ce_identity(), CERoles.PLC_CHANNEL_TERMINAL, new_ce_identity(), "PLC:X1")
    terminal = TerminalEndpoint(new_ce_identity(), CERoles.CABINET_TERMINAL, new_ce_identity(), "TB1:01")
    device = TerminalEndpoint(new_ce_identity(), CERoles.DEVICE_TERMINAL, new_ce_identity(), "LS1:1")
    first = WireSegment(new_ce_identity(), plc.identity, terminal.identity, "W-001", "18 AWG", "BK", "DI", specified_length_mm=100)
    second = WireSegment(new_ce_identity(), terminal.identity, device.identity, "W-002", "18 AWG", "BK", "DI", specified_length_mm=200)
    return ElectricalConnectionPath(new_ce_identity(), new_ce_identity(), "DI-001", (plc, terminal, device), (first, second))


def test_terminal_plan_projects_both_sides_of_a_cabinet_terminal():
    path = _path()
    rows = terminal_plan_rows((path,))
    assert [row["WireTag"] for row in rows] == ["W-001", "W-002"]
    assert {row["RemoteTerminal"] for row in rows} == {"PLC:X1", "LS1:1"}
    assert all(row["TerminalDesignation"] == "TB1:01" for row in rows)
    assert "TB1:01" in terminal_plan_csv((path,))

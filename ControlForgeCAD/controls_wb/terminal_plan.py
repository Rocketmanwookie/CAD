# SPDX-License-Identifier: MIT
"""Deterministic terminal-plan projections from canonical electrical paths."""

from __future__ import annotations

import csv
from io import StringIO

from controls_wb.electrical_path import ElectricalConnectionPath
from controls_wb.identity import CERoles


TERMINAL_PLAN_HEADERS = (
    "TerminalOwnerIdentity", "TerminalIdentity", "TerminalDesignation", "TerminalLabel",
    "SignalIdentity", "SignalTag", "WireIdentity", "WireTag", "RemoteTerminalIdentity",
    "RemoteTerminal", "ConductorSize", "Color", "CircuitFunction", "LengthMm",
)


def terminal_plan_rows(paths: tuple[ElectricalConnectionPath, ...]) -> list[dict[str, object]]:
    """Return one stable row per cabinet terminal/wire-side connection."""

    rows: list[dict[str, object]] = []
    for path in paths:
        path.validate()
        for index, terminal in enumerate(path.terminals):
            if terminal.role != CERoles.CABINET_TERMINAL:
                continue
            for wire_index in (index - 1, index):
                if wire_index < 0 or wire_index >= len(path.wires):
                    continue
                wire = path.wires[wire_index]
                remote = path.terminals[wire_index if wire_index + 1 == index else wire_index + 1]
                rows.append({
                    "TerminalOwnerIdentity": terminal.owner_identity,
                    "TerminalIdentity": terminal.identity,
                    "TerminalDesignation": terminal.designation,
                    "TerminalLabel": terminal.label,
                    "SignalIdentity": path.signal_identity,
                    "SignalTag": path.signal_tag,
                    "WireIdentity": wire.identity,
                    "WireTag": wire.wire_tag,
                    "RemoteTerminalIdentity": remote.identity,
                    "RemoteTerminal": remote.designation,
                    "ConductorSize": wire.conductor_size,
                    "Color": wire.color,
                    "CircuitFunction": wire.circuit_function,
                    "LengthMm": wire.effective_length_mm,
                })
    return sorted(rows, key=lambda row: (
        str(row["TerminalOwnerIdentity"]), str(row["TerminalDesignation"]), str(row["WireTag"]),
    ))


def terminal_plan_csv(paths: tuple[ElectricalConnectionPath, ...]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=TERMINAL_PLAN_HEADERS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(terminal_plan_rows(paths))
    return output.getvalue()

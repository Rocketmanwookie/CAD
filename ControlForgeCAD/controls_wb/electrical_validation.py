# SPDX-License-Identifier: MIT
"""Whole-project semantic validation for continuous electrical paths."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from controls_wb.electrical_path import ElectricalConnectionPath


@dataclass(frozen=True)
class ElectricalGraphFinding:
    severity: str
    code: str
    identity: str
    message: str


def validate_connection_graph(
    paths: Iterable[ElectricalConnectionPath],
    *,
    known_owner_identities: set[str] | frozenset[str],
    known_signal_identities: set[str] | frozenset[str],
) -> tuple[ElectricalGraphFinding, ...]:
    """Validate identity uniqueness and references across all connection paths."""

    findings: list[ElectricalGraphFinding] = []
    identity_kind: dict[str, str] = {}
    terminal_signal: dict[str, str] = {}
    signal_tag: dict[str, str] = {}

    def register(identity: str, kind: str) -> None:
        previous = identity_kind.get(identity)
        if previous is not None:
            findings.append(
                ElectricalGraphFinding(
                    "ERROR",
                    "duplicate_identity",
                    identity,
                    f"CE identity is used by both {previous} and {kind}.",
                )
            )
        else:
            identity_kind[identity] = kind

    for path in paths:
        try:
            path.validate()
        except ValueError as exc:
            findings.append(
                ElectricalGraphFinding("ERROR", "invalid_path", path.identity, str(exc))
            )
            continue
        register(path.identity, "connection_path")
        if path.signal_identity not in known_signal_identities:
            findings.append(
                ElectricalGraphFinding(
                    "ERROR",
                    "dangling_signal",
                    path.signal_identity,
                    f"Path {path.identity} references an unknown signal.",
                )
            )
        previous_tag = signal_tag.get(path.signal_identity)
        if previous_tag is not None and previous_tag != path.signal_tag:
            findings.append(
                ElectricalGraphFinding(
                    "ERROR",
                    "signal_tag_conflict",
                    path.signal_identity,
                    f"Signal is represented by conflicting tags {previous_tag!r} and {path.signal_tag!r}.",
                )
            )
        signal_tag[path.signal_identity] = path.signal_tag

        for terminal in path.terminals:
            previous_signal = terminal_signal.get(terminal.identity)
            if previous_signal is None:
                register(terminal.identity, "terminal")
                terminal_signal[terminal.identity] = path.signal_identity
            elif previous_signal != path.signal_identity:
                findings.append(
                    ElectricalGraphFinding(
                        "ERROR",
                        "terminal_signal_conflict",
                        terminal.identity,
                        "Terminal is assigned to connection paths for different signals.",
                    )
                )
            if terminal.owner_identity not in known_owner_identities:
                findings.append(
                    ElectricalGraphFinding(
                        "ERROR",
                        "dangling_terminal_owner",
                        terminal.identity,
                        f"Terminal references unknown owner {terminal.owner_identity}.",
                    )
                )
        for wire in path.wires:
            register(wire.identity, "wire")
            if not wire.conductor_size:
                findings.append(
                    ElectricalGraphFinding(
                        "WARNING", "missing_conductor_size", wire.identity, "Wire has no conductor size."
                    )
                )
            if not wire.color:
                findings.append(
                    ElectricalGraphFinding(
                        "WARNING", "missing_wire_color", wire.identity, "Wire has no approved color."
                    )
                )
            if wire.effective_length_mm is None:
                findings.append(
                    ElectricalGraphFinding(
                        "WARNING", "missing_wire_length", wire.identity, "Wire has no routed or specified length."
                    )
                )

    return tuple(
        sorted(findings, key=lambda item: (item.severity, item.code, item.identity, item.message))
    )

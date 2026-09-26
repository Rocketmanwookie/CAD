# SPDX-License-Identifier: MIT
"""Pure allocation-delta preflight for safe PLC occurrence reconciliation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from controls_wb.io_list import IOSignal


@dataclass(frozen=True)
class AllocationDelta:
    """One logical I/O point's current/proposed physical allocation change."""

    tag: str
    signal_type: str
    current: IOSignal | None
    proposed: IOSignal | None

    @property
    def kind(self) -> str:
        if self.current is None:
            return "added"
        if self.proposed is None:
            return "removed"
        if self.current.signal_type != self.proposed.signal_type:
            return "type_changed"
        if _coordinate(self.current) != _coordinate(self.proposed):
            return "moved"
        return "unchanged"


def allocation_delta(current: Iterable[IOSignal], proposed: Iterable[IOSignal]) -> tuple[AllocationDelta, ...]:
    """Compare unique logical tags without mutating project or FreeCAD state."""

    current_by_tag = _by_tag(current, "current")
    proposed_by_tag = _by_tag(proposed, "proposed")
    return tuple(
        AllocationDelta(tag, (current_by_tag.get(tag) or proposed_by_tag[tag]).signal_type,
                        current_by_tag.get(tag), proposed_by_tag.get(tag))
        for tag in sorted(set(current_by_tag) | set(proposed_by_tag))
    )


def preflight_reconciliation(current: Iterable[IOSignal], proposed: Iterable[IOSignal], dependent_tags: Iterable[str] = ()) -> tuple[AllocationDelta, ...]:
    """Reject unsafe removal/type changes before an allocation is persisted.

    A same-type move is intentionally returned for a later atomic FreeCAD
    migration; a removed logical point with a path and every type change require
    explicit engineering action instead of silent graph mutation.
    """

    dependencies = frozenset(dependent_tags)
    delta = allocation_delta(current, proposed)
    blocked = [item for item in delta if item.kind == "type_changed" or item.kind == "removed" and item.tag in dependencies]
    if blocked:
        details = "; ".join(f"{item.tag}: {item.kind}" for item in blocked)
        raise ValueError(f"Unsafe PLC allocation reconciliation requires explicit migration: {details}")
    return delta


def _by_tag(signals: Iterable[IOSignal], label: str) -> dict[str, IOSignal]:
    result = {}
    for signal in signals:
        if signal.tag in result:
            raise ValueError(f"Duplicate {label} allocation signal tag {signal.tag!r}.")
        result[signal.tag] = signal
    return result


def _coordinate(signal: IOSignal) -> tuple[str, str, str]:
    return signal.rack, signal.slot, signal.channel

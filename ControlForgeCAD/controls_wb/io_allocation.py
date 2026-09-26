# SPDX-License-Identifier: MIT
"""Deterministic PLC rack/slot/channel allocation for canonical I/O signals.

This module is deliberately FreeCAD-independent.  It turns the selected PLC
catalog record and a list of logical I/O signals into an explicit rack/slot/
channel projection without claiming vendor project-file compatibility.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

from controls_wb.hardware_catalog import HardwareCatalog, HardwarePart, line_catalog, part_by_name
from controls_wb.io_list import IOSignal


_CAPACITY_KEY_BY_SIGNAL_TYPE = {
    "digital_input": "di",
    "digital_output": "do",
    "analog_input": "ai",
    "analog_output": "ao",
}


@dataclass(frozen=True)
class PLCModuleAllocation:
    """One catalog-backed PLC CPU or expansion-module placement in a rack."""

    rack: str
    slot: str
    module_name: str
    part_number: str
    source_id: str
    is_cpu: bool = False


@dataclass(frozen=True)
class IOAllocationFinding:
    """A deterministic capacity, collision, or compatibility result."""

    severity: str
    code: str
    signal_tag: str
    message: str


@dataclass(frozen=True)
class IOAllocationResult:
    """Allocated signal projection plus the module occurrences and findings."""

    signals: tuple[IOSignal, ...]
    modules: tuple[PLCModuleAllocation, ...]
    findings: tuple[IOAllocationFinding, ...]


@dataclass(frozen=True)
class AllocationPreviewRow:
    """One immutable catalog allocation row with an editable engineering label."""

    signal_tag: str
    signal_type: str
    engineering_label: str
    rack: str
    slot: str
    channel: str
    plc_terminal: str
    module_name: str
    part_number: str


def allocate_io_signals(
    signals: Iterable[IOSignal],
    catalog: HardwareCatalog,
    make: str,
    line: str,
    cpu_name: str,
    *,
    rack: str = "0",
    cpu_slot: str = "1",
) -> IOAllocationResult:
    """Allocate supported I/O signals to a selected CPU and catalog modules.

    Slots are deterministic: the CPU occupies ``cpu_slot`` and expansion
    modules are assigned increasing integer slots after it.  Channels are zero
    based within their module.  Unsupported signal types remain unchanged with
    an actionable finding instead of receiving an invented allocation.
    """

    requested = tuple(signals)
    line_data = line_catalog(catalog, make, line)
    if line_data is None:
        return _unavailable_result(requested, "unknown_plc_line", f"No catalog line matches {make} {line}.")
    cpu = part_by_name(line_data.cpus, cpu_name)
    if cpu is None:
        return _unavailable_result(requested, "unknown_plc_cpu", f"No catalog CPU matches {cpu_name!r}.")

    allocated: list[IOSignal] = list(requested)
    modules: list[PLCModuleAllocation] = [
        PLCModuleAllocation(str(rack), str(cpu_slot), cpu.name, cpu.part_number, cpu.source_id, is_cpu=True)
    ]
    findings: list[IOAllocationFinding] = []
    next_slot = _next_slot(cpu_slot)

    for signal_type, capacity_key in _CAPACITY_KEY_BY_SIGNAL_TYPE.items():
        indexes = [index for index, signal in enumerate(allocated) if signal.signal_type == signal_type]
        capacity = int(getattr(cpu, capacity_key))
        cpu_indexes, remaining_indexes = indexes[:capacity], indexes[capacity:]
        for channel, index in enumerate(cpu_indexes):
            allocated[index] = _allocated(allocated[index], rack, cpu_slot, channel, cpu)

        module = _best_module(line_data.io_modules, capacity_key)
        while remaining_indexes and module is not None:
            slot = str(next_slot)
            next_slot += 1
            modules.append(PLCModuleAllocation(str(rack), slot, module.name, module.part_number, module.source_id))
            module_capacity = int(getattr(module, capacity_key))
            for channel in range(module_capacity):
                if not remaining_indexes:
                    break
                index = remaining_indexes.pop(0)
                allocated[index] = _allocated(allocated[index], rack, slot, channel, module)

        for index in remaining_indexes:
            signal = allocated[index]
            findings.append(
                IOAllocationFinding(
                    "ERROR",
                    "insufficient_io_capacity",
                    signal.tag,
                    f"No selected catalog capacity remains for {signal.signal_type} signal {signal.tag}.",
                )
            )

    for index, signal in enumerate(allocated):
        if signal.signal_type not in _CAPACITY_KEY_BY_SIGNAL_TYPE:
            findings.append(
                IOAllocationFinding(
                    "WARNING",
                    "unsupported_io_signal_type",
                    signal.tag,
                    f"Signal {signal.tag} has unsupported type {signal.signal_type!r} and was not allocated.",
                )
            )

    findings.extend(validate_io_allocations(allocated))
    return IOAllocationResult(tuple(allocated), tuple(modules), _sorted_findings(findings))


def allocation_preview_rows(result: IOAllocationResult) -> tuple[AllocationPreviewRow, ...]:
    """Return catalog part/channel rows suitable for review before persistence."""

    module_by_coordinate = {(module.rack, module.slot): module for module in result.modules}
    rows = []
    for signal in result.signals:
        module = module_by_coordinate.get((signal.rack, signal.slot))
        if not signal.rack or not signal.slot or not signal.channel or module is None:
            continue
        rows.append(
            AllocationPreviewRow(
                signal_tag=signal.tag,
                signal_type=signal.signal_type,
                engineering_label=signal.description or signal.device,
                rack=signal.rack,
                slot=signal.slot,
                channel=signal.channel,
                plc_terminal=signal.address,
                module_name=module.module_name,
                part_number=module.part_number,
            )
        )
    return tuple(rows)


def apply_engineering_labels(
    result: IOAllocationResult, labels_by_signal_tag: dict[str, str]
) -> IOAllocationResult:
    """Apply readable labels without changing canonical allocation keys or tags."""

    signals = []
    for signal in result.signals:
        label = str(labels_by_signal_tag.get(signal.tag, "")).strip()
        signals.append(replace(signal, description=label or signal.description, device=label or signal.device))
    return replace(result, signals=tuple(signals))


def _allocated(signal: IOSignal, rack: str, slot: str, channel: int, module: HardwarePart) -> IOSignal:
    return replace(
        signal,
        rack=str(rack),
        slot=str(slot),
        channel=str(channel),
        module_name=module.name,
        catalog_part_number=module.part_number,
        mapping_status="allocated",
    )


def _best_module(modules: Iterable[HardwarePart], capacity_key: str) -> HardwarePart | None:
    compatible = [module for module in modules if int(getattr(module, capacity_key)) > 0]
    if not compatible:
        return None
    return min(compatible, key=lambda module: (int(getattr(module, capacity_key)), module.part_number, module.name))


def _next_slot(cpu_slot: str) -> int:
    try:
        return int(str(cpu_slot)) + 1
    except ValueError as exc:
        raise ValueError("CPU slot must be an integer for deterministic module allocation.") from exc


def validate_io_allocations(signals: Iterable[IOSignal]) -> tuple[IOAllocationFinding, ...]:
    """Report duplicate manually entered or imported PLC channel assignments."""

    seen: dict[tuple[str, str, str, str], str] = {}
    findings: list[IOAllocationFinding] = []
    for signal in signals:
        if not (signal.rack and signal.slot and signal.channel):
            continue
        key = (signal.rack, signal.slot, signal.signal_type, signal.channel)
        previous = seen.get(key)
        if previous:
            findings.append(
                IOAllocationFinding(
                    "ERROR", "io_channel_collision", signal.tag,
                    f"Signals {previous} and {signal.tag} share rack {key[0]}, slot {key[1]}, "
                    f"{key[2]} channel {key[3]}.",
                )
            )
        else:
            seen[key] = signal.tag
    return _sorted_findings(findings)


def _unavailable_result(signals: tuple[IOSignal, ...], code: str, message: str) -> IOAllocationResult:
    return IOAllocationResult(
        signals,
        (),
        _sorted_findings(
            IOAllocationFinding("ERROR", code, signal.tag, message) for signal in signals
        ),
    )


def _sorted_findings(findings: Iterable[IOAllocationFinding]) -> tuple[IOAllocationFinding, ...]:
    return tuple(sorted(findings, key=lambda item: (item.severity, item.code, item.signal_tag, item.message)))

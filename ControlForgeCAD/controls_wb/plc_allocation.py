# SPDX-License-Identifier: MIT
"""Immutable PLC allocation domain; no document mutation or vendor address guesses.

Channels are numbered within each module and signal type. A rack references an
existing controller identity, not a replacement controller occurrence. HardwarePart
is the caller's catalog definition, never an occurrence identity. This bounded
model permits one rack per controller and models signal modules only, not boards.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Mapping

from controls_wb.hardware_catalog import HardwarePart
from controls_wb.identity import is_ce_identity, new_ce_identity


_CAPACITIES = {
    "digital_input": "di",
    "digital_output": "do",
    "analog_input": "ai",
    "analog_output": "ao",
}
_AREAS = {
    "digital_input": "I", "analog_input": "I",
    "digital_output": "Q", "analog_output": "Q",
}


def _identity(value: str) -> None:
    if not isinstance(value, str) or not is_ce_identity(value):
        raise ValueError(f"Invalid canonical CE identity: {value!r}")


def _integer(value: int, label: str, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}.")


def _signal_type(value: str) -> None:
    if value not in _CAPACITIES:
        raise ValueError(f"Unsupported allocation signal type: {value!r}")


def _part(part: HardwarePart) -> None:
    if not isinstance(part, HardwarePart) or not part.part_number.strip():
        raise ValueError("Allocation requires a catalog HardwarePart with a part number.")
    for attribute in _CAPACITIES.values():
        _integer(getattr(part, attribute), f"Catalog {attribute} capacity")
    if part.max_signal_modules is not None:
        _integer(part.max_signal_modules, "CPU signal-module limit")


@dataclass(frozen=True)
class AddressInterval:
    """Explicit half-open bit interval [start_bit, start_bit + width_bits).

Profile records the caller's addressing policy, not an independent address space:
different profiles can still collide within the same controller and I/Q area.
No byte alignment, reserved ranges, or vendor maximum is inferred here.
"""

    controller_identity: str
    area: str
    start_bit: int
    width_bits: int
    profile: str

    def __post_init__(self):
        _identity(self.controller_identity)
        if self.area not in {"I", "Q"}:
            raise ValueError("Address area must be I or Q.")
        _integer(self.start_bit, "Address start bit")
        _integer(self.width_bits, "Address width", 1)
        if not isinstance(self.profile, str) or not self.profile.strip():
            raise ValueError("An explicit address profile is required.")

    @property
    def end_bit(self) -> int:
        return self.start_bit + self.width_bits


@dataclass(frozen=True)
class Rack:
    identity: str
    controller_identity: str
    cpu: HardwarePart

    def __post_init__(self):
        _identity(self.identity)
        _identity(self.controller_identity)
        if self.identity == self.controller_identity:
            raise ValueError("Rack and controller identities must be distinct.")
        _part(self.cpu)


@dataclass(frozen=True)
class Channel:
    identity: str
    module_identity: str
    signal_type: str
    index: int
    address: AddressInterval | None = None

    def __post_init__(self):
        _identity(self.identity)
        _identity(self.module_identity)
        _signal_type(self.signal_type)
        _integer(self.index, "Channel index")
        if self.address is not None:
            if not isinstance(self.address, AddressInterval):
                raise ValueError("Channel address must be an AddressInterval or None.")
            if self.address.area != _AREAS[self.signal_type]:
                raise ValueError("Channel signal type does not match address area.")


@dataclass(frozen=True)
class Module:
    identity: str
    rack_identity: str
    slot: int
    part: HardwarePart
    channels: tuple[Channel, ...]
    onboard: bool = False

    def __post_init__(self):
        _identity(self.identity)
        _identity(self.rack_identity)
        _integer(self.slot, "Module slot")
        _part(self.part)
        if type(self.onboard) is not bool:
            raise ValueError("Onboard must be a boolean.")
        object.__setattr__(self, "channels", tuple(self.channels))
        expected = {
            (kind, index)
            for kind, attribute in _CAPACITIES.items()
            for index in range(getattr(self.part, attribute))
        }
        actual = [(channel.signal_type, channel.index) for channel in self.channels]
        if len(actual) != len(set(actual)) or set(actual) != expected:
            raise ValueError("Module channels must exactly match catalog type capacities.")
        if any(channel.module_identity != self.identity for channel in self.channels):
            raise ValueError("Channel references the wrong module identity.")


@dataclass(frozen=True)
class Assignment:
    """A relation between existing identities, not a newly identified entity."""

    signal_identity: str
    signal_type: str
    channel_identity: str

    def __post_init__(self):
        _identity(self.signal_identity)
        _identity(self.channel_identity)
        _signal_type(self.signal_type)


def module_from_catalog(
    rack: Rack,
    part: HardwarePart,
    slot: int,
    *,
    identity: str | None = None,
    onboard: bool = False,
    address_bases: Mapping[str, AddressInterval] | None = None,
) -> Module:
    """Create one occurrence with fresh channel IDs; persist the returned record.

Each supplied interval is channel zero's explicit base/width/profile for its
signal type. Subsequent channels are packed at that width. Missing types remain
unresolved. Calling this constructor twice creates two distinct occurrences;
allocation itself never generates identities. Catalog membership and electrical
compatibility must be established by the caller.
"""
    _part(part)
    bases = dict(address_bases or {})
    for kind, base in bases.items():
        _signal_type(kind)
        if not isinstance(base, AddressInterval):
            raise ValueError("Address bases must be AddressInterval records.")
        if base.controller_identity != rack.controller_identity or base.area != _AREAS[kind]:
            raise ValueError("Address base has the wrong controller or area.")
        if getattr(part, _CAPACITIES[kind]) == 0:
            raise ValueError("Address base supplied for a type with no catalog channels.")
    module_id = new_ce_identity() if identity is None else identity
    channels = []
    for kind, attribute in _CAPACITIES.items():
        base = bases.get(kind)
        for index in range(getattr(part, attribute)):
            address = replace(base, start_bit=base.start_bit + index * base.width_bits) if base else None
            channels.append(Channel(new_ce_identity(), module_id, kind, index, address))
    module = Module(module_id, rack.identity, slot, part, tuple(channels), onboard)
    validate_allocation((rack,), (module,))
    return module


def validate_allocation(
    racks: tuple[Rack, ...],
    modules: tuple[Module, ...],
    assignments: tuple[Assignment, ...] = (),
) -> tuple[str, ...]:
    """Raise ValueError for invalid state; return sorted unresolved-input notices.

All configured channel ranges are checked, including currently unassigned ones.
Unknown CPU expansion limits and assigned channels without addresses are notices,
not evidence that the configuration is fully verified.
"""
    identities: set[str] = set()

    def claim(identity: str):
        if identity in identities:
            raise ValueError(f"Duplicate allocation identity: {identity}")
        identities.add(identity)

    rack_index = {}
    for rack in racks:
        claim(rack.identity)
        claim(rack.controller_identity)
        rack_index[rack.identity] = rack
    channels = {}
    slots = set()
    onboard_racks = set()
    expansion_counts = {rack.identity: 0 for rack in racks}
    ranges: dict[tuple[str, str], list[tuple[int, int, str]]] = {}
    for module in modules:
        claim(module.identity)
        rack = rack_index.get(module.rack_identity)
        if rack is None:
            raise ValueError("Module references a missing rack.")
        slot_key = (rack.identity, module.slot)
        if slot_key in slots:
            raise ValueError(f"Duplicate module slot: {module.slot}")
        slots.add(slot_key)
        if module.onboard:
            if rack.identity in onboard_racks or module.part != rack.cpu:
                raise ValueError("Onboard module must uniquely represent the rack CPU part.")
            onboard_racks.add(rack.identity)
        else:
            expansion_counts[rack.identity] += 1
        for channel in module.channels:
            claim(channel.identity)
            channels[channel.identity] = channel
            address = channel.address
            if address is not None:
                if address.controller_identity != rack.controller_identity:
                    raise ValueError("Channel address references the wrong controller.")
                ranges.setdefault((address.controller_identity, address.area), []).append(
                    (address.start_bit, address.end_bit, channel.identity)
                )
    notices = []
    for rack in racks:
        count = expansion_counts[rack.identity]
        limit = rack.cpu.max_signal_modules
        if count and limit is None:
            notices.append(f"Rack {rack.identity}: CPU signal-module limit is unresolved.")
        elif limit is not None and count > limit:
            raise ValueError(f"Rack {rack.identity}: {count} signal modules exceed CPU limit {limit}.")
    for key, intervals in sorted(ranges.items()):
        ordered = sorted(intervals)
        for previous, current in zip(ordered, ordered[1:]):
            if current[0] < previous[1]:
                raise ValueError(f"Address overlap in controller/area {key}: {previous[2]} and {current[2]}.")
    occupied = set()
    for assignment in assignments:
        claim(assignment.signal_identity)
        channel = channels.get(assignment.channel_identity)
        if channel is None:
            raise ValueError("Assignment references a missing channel.")
        if channel.signal_type != assignment.signal_type:
            raise ValueError("Assignment signal type does not match channel type.")
        if channel.identity in occupied:
            raise ValueError("Channel is assigned to more than one signal.")
        occupied.add(channel.identity)
        if channel.address is None:
            notices.append(f"Signal {assignment.signal_identity}: channel address is unresolved.")
    return tuple(sorted(notices))


def allocate_signals(
    racks: tuple[Rack, ...],
    modules: tuple[Module, ...],
    signals: Mapping[str, str],
    assignments: tuple[Assignment, ...] = (),
) -> tuple[Assignment, ...]:
    """Assign persisted signal IDs to free channels without mutating input state.

Existing assignments are retained, including signals absent from this request.
New signals sort by identity; channels sort by rack identity, slot, type, index.
Repeated calls over the same occurrences return equal, signal-ID-sorted results.
The caller must establish that supplied signal IDs are actually persisted.
"""
    validate_allocation(racks, modules, assignments)
    requested = dict(signals)
    for identity, kind in requested.items():
        _identity(identity)
        _signal_type(kind)
    existing = {item.signal_identity: item for item in assignments}
    occupied = {item.channel_identity for item in assignments}
    available = sorted(
        ((module.rack_identity, module.slot, channel.signal_type, channel.index, channel)
         for module in modules for channel in module.channels),
        key=lambda item: item[:4],
    )
    result = list(assignments)
    for identity, kind in sorted(requested.items()):
        if identity in existing:
            if existing[identity].signal_type != kind:
                raise ValueError("Existing assignment conflicts with requested signal type.")
            continue
        channel = next((item[4] for item in available
                        if item[4].signal_type == kind and item[4].identity not in occupied), None)
        if channel is None:
            raise ValueError(f"No free {kind} channel for signal {identity}.")
        result.append(Assignment(identity, kind, channel.identity))
        occupied.add(channel.identity)
    ordered = tuple(sorted(result, key=lambda item: item.signal_identity))
    validate_allocation(racks, modules, ordered)
    return ordered

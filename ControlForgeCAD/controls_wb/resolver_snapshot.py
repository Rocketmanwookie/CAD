# SPDX-License-Identifier: MIT
"""Immutable, review-only snapshots of resolved controls requirements.

Release 1 snapshots bind typed load, I/O, and generic hardware proposals into
one deterministic planning record.  The capacity envelope is intentionally a
counting aid: it never declares enclosure fit, thermal compliance, ratings,
or an approved physical design.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from math import ceil

from controls_wb.identity import imported_ce_identity, is_ce_identity
from controls_wb.load_requirements import (
    HardwareRequirement,
    IORequirement,
    LoadRequirement,
    hardware_requirements_from_project,
    io_requirements_from_project,
    load_requirements_from_project,
)


SNAPSHOT_VERSION = "resolver-snapshot.v1"
CAPACITY_CALCULATION_VERSION = "panel-capacity-envelope.v1"


@dataclass(frozen=True)
class PanelCapacityEnvelope:
    """Explicit planning counts, not a physical or electrical design result."""

    identity: str
    project_identity: str
    snapshot_identity: str
    equipment_unit_count: int
    terminal_connection_count: int
    reserve_percent: int | None
    reserve_equipment_units: int | None
    required_equipment_units: int | None
    rail_positions: int | None
    terminal_positions: int | None
    heat_input: str | None
    power_input: str | None
    counts_by_requirement_class: tuple[tuple[str, int], ...]
    unresolved_inputs: tuple[str, ...]
    calculation_version: str = CAPACITY_CALCULATION_VERSION

    def validate(self) -> None:
        if not all(is_ce_identity(value) for value in (self.identity, self.project_identity, self.snapshot_identity)):
            raise ValueError("Panel capacity envelope identities must be valid CE identities.")
        if self.equipment_unit_count < 0 or self.terminal_connection_count < 0:
            raise ValueError("Panel capacity counts cannot be negative.")
        if self.reserve_percent is not None and (isinstance(self.reserve_percent, bool) or self.reserve_percent < 0):
            raise ValueError("Panel capacity reserve percent must be a non-negative integer when supplied.")
        if self.reserve_percent is None and any(value is not None for value in (self.reserve_equipment_units, self.required_equipment_units)):
            raise ValueError("Panel capacity reserve results require an explicit reserve percent.")
        if self.reserve_percent is not None and (self.reserve_equipment_units is None or self.required_equipment_units is None):
            raise ValueError("Panel capacity reserve results are required when reserve percent is supplied.")
        if any(not key or value <= 0 for key, value in self.counts_by_requirement_class):
            raise ValueError("Panel capacity requirement-class counts must be positive.")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        payload = asdict(self)
        payload["counts_by_requirement_class"] = [
            {"requirement_class": name, "quantity": quantity}
            for name, quantity in self.counts_by_requirement_class
        ]
        payload["unresolved_inputs"] = list(self.unresolved_inputs)
        return payload


@dataclass(frozen=True)
class ResolverSnapshot:
    """A deterministic common source for later Release 1 export adapters."""

    identity: str
    project_identity: str
    loads: tuple[LoadRequirement, ...]
    io_requirements: tuple[IORequirement, ...]
    hardware_requirements: tuple[HardwareRequirement, ...]
    capacity_envelope: PanelCapacityEnvelope
    source_schema_version: str = ""
    review_status: str = "blocked_missing_input"
    version: str = SNAPSHOT_VERSION

    def validate(self) -> None:
        if not is_ce_identity(self.identity) or not is_ce_identity(self.project_identity):
            raise ValueError("Resolver snapshot identities must be valid CE identities.")
        if self.capacity_envelope.project_identity != self.project_identity:
            raise ValueError("Panel capacity envelope belongs to a different project.")
        if self.capacity_envelope.snapshot_identity != self.identity:
            raise ValueError("Panel capacity envelope belongs to a different snapshot.")
        if self.review_status not in {"review", "blocked_missing_input"}:
            raise ValueError("Resolver snapshot review status is unsupported.")
        self.capacity_envelope.validate()
        for requirement in (*self.loads, *self.io_requirements, *self.hardware_requirements):
            requirement.validate()
        if len({item.identity for item in self.loads}) != len(self.loads):
            raise ValueError("Resolver snapshot contains duplicate load identities.")
        if len({item.identity for item in self.io_requirements}) != len(self.io_requirements):
            raise ValueError("Resolver snapshot contains duplicate I/O requirement identities.")
        if len({item.identity for item in self.hardware_requirements}) != len(self.hardware_requirements):
            raise ValueError("Resolver snapshot contains duplicate hardware requirement identities.")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "identity": self.identity,
            "project_identity": self.project_identity,
            "version": self.version,
            "source_schema_version": self.source_schema_version,
            "review_status": self.review_status,
            "loads": [item.to_dict() for item in self.loads],
            "io_requirements": [item.to_dict() for item in self.io_requirements],
            "hardware_requirements": [item.to_dict() for item in self.hardware_requirements],
            "capacity_envelope": self.capacity_envelope.to_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))


def resolver_snapshot_from_project(project: object, reserve_percent: int | None = None) -> ResolverSnapshot:
    """Build a deterministic snapshot from persisted M4.1 requirement records.

    ``reserve_percent`` is an explicit planning input.  Omitting it deliberately
    leaves reserve-related capacity values unresolved instead of inventing a
    panel-sizing policy.
    """

    project_identity = str(getattr(project, "CEIdentity", "") or "")
    if not is_ce_identity(project_identity):
        raise ValueError("Resolver snapshot requires a project CE identity.")
    if reserve_percent is not None and (isinstance(reserve_percent, bool) or not isinstance(reserve_percent, int) or reserve_percent < 0):
        raise ValueError("Reserve percent must be a non-negative integer when supplied.")

    loads = tuple(sorted(load_requirements_from_project(project), key=lambda item: item.identity))
    io_requirements = tuple(sorted(io_requirements_from_project(project), key=lambda item: item.identity))
    hardware_requirements = tuple(sorted(hardware_requirements_from_project(project), key=lambda item: item.identity))
    _validate_links(loads, io_requirements, hardware_requirements)

    material = json.dumps(
        {
            "version": SNAPSHOT_VERSION,
            "project": project_identity,
            "loads": [item.to_dict() for item in loads],
            "io": [item.to_dict() for item in io_requirements],
            "hardware": [item.to_dict() for item in hardware_requirements],
            "reserve_percent": reserve_percent,
            "source_schema_version": str(getattr(project, "SchemaVersion", "") or ""),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    identity = imported_ce_identity("resolver-snapshot", material)
    envelope = panel_capacity_envelope(project_identity, identity, hardware_requirements, reserve_percent)
    snapshot = ResolverSnapshot(
        identity,
        project_identity,
        loads,
        io_requirements,
        hardware_requirements,
        envelope,
        str(getattr(project, "SchemaVersion", "") or ""),
        "blocked_missing_input" if envelope.unresolved_inputs else "review",
    )
    snapshot.validate()
    return snapshot


def panel_capacity_envelope(
    project_identity: str,
    snapshot_identity: str,
    hardware_requirements: tuple[HardwareRequirement, ...],
    reserve_percent: int | None = None,
) -> PanelCapacityEnvelope:
    """Count explicit proposal units and expose all still-unresolved inputs."""

    if not is_ce_identity(project_identity) or not is_ce_identity(snapshot_identity):
        raise ValueError("Panel capacity envelope requires project and snapshot CE identities.")
    if reserve_percent is not None and (isinstance(reserve_percent, bool) or not isinstance(reserve_percent, int) or reserve_percent < 0):
        raise ValueError("Reserve percent must be a non-negative integer when supplied.")
    for requirement in hardware_requirements:
        requirement.validate()

    counts: dict[str, int] = {}
    unresolved = {"thermal_power_input_not_calculated", "physical_fit_not_calculated"}
    for requirement in hardware_requirements:
        counts[requirement.requirement_class] = counts.get(requirement.requirement_class, 0) + requirement.quantity
        unresolved.update(requirement.unresolved_fields)
    if reserve_percent is None:
        unresolved.add("reserve_policy_not_provided")
        reserve_units = None
        required_units = None
    else:
        reserve_units = ceil(sum(counts.values()) * reserve_percent / 100)
        required_units = sum(counts.values()) + reserve_units

    envelope = PanelCapacityEnvelope(
        identity=imported_ce_identity("panel-capacity-envelope", f"{project_identity}:{snapshot_identity}"),
        project_identity=project_identity,
        snapshot_identity=snapshot_identity,
        equipment_unit_count=sum(counts.values()),
        terminal_connection_count=counts.get("terminal_connection", 0),
        reserve_percent=reserve_percent,
        reserve_equipment_units=reserve_units,
        required_equipment_units=required_units,
        rail_positions=None,
        terminal_positions=None,
        heat_input=None,
        power_input=None,
        counts_by_requirement_class=tuple(sorted(counts.items())),
        unresolved_inputs=tuple(sorted(unresolved | {
            "rail_positions_not_calculated",
            "terminal_positions_not_calculated",
            "heat_input_not_calculated",
            "power_input_not_calculated",
        })),
    )
    envelope.validate()
    return envelope


def _validate_links(
    loads: tuple[LoadRequirement, ...],
    io_requirements: tuple[IORequirement, ...],
    hardware_requirements: tuple[HardwareRequirement, ...],
) -> None:
    load_ids = {item.identity for item in loads}
    io_ids = {item.identity for item in io_requirements}
    if any(item.load_identity not in load_ids for item in io_requirements):
        raise ValueError("Resolver snapshot contains an I/O requirement with an unknown load identity.")
    if any(item.load_identity not in load_ids for item in hardware_requirements):
        raise ValueError("Resolver snapshot contains a hardware requirement with an unknown load identity.")
    if any(identity not in io_ids for item in hardware_requirements for identity in item.linked_io_identities):
        raise ValueError("Resolver snapshot contains a hardware requirement with an unknown I/O identity.")

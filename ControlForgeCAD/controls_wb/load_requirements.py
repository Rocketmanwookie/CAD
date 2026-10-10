# SPDX-License-Identifier: MIT
"""Typed, reviewable controls-load and I/O requirements for Release 1.

This module deliberately proposes *hardware classes*, never electrical ratings,
vendor parts, safety functions, or approval decisions.  It provides the stable
input records that later panel-capacity and export adapters consume.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from controls_wb.identity import imported_ce_identity


LOAD_CLASSES = frozenset({"motor", "conveyor", "hydraulic", "robot", "generic"})
IO_DIRECTIONS = frozenset({"input", "output", "analog_input", "analog_output"})
CONTROL_MODES = frozenset({"on_off", "speed_control", "position_control", "process_control", "unknown"})
DRIVE_TYPES = frozenset({"electric_motor", "pneumatic", "hydraulic", "combustion", "none", "unknown"})
RESOLUTION_NEEDS_ENGINEERING_DECISION = "needs_engineering_decision"


@dataclass(frozen=True)
class LoadRequirement:
    """A described controlled load, independent of physical CAD realization."""

    identity: str
    tag: str
    load_class: str
    description: str
    quantity: int = 1
    control_mode: str = "unknown"
    supply_voltage: str = ""
    power: str = ""
    current: str = ""
    duty: str = ""
    environment: str = ""
    drive_type: str = "unknown"
    evidence_locator: str = ""

    def validate(self) -> None:
        if not self.identity.strip():
            raise ValueError("Load requirement identity is required.")
        if not self.tag.strip():
            raise ValueError("Load requirement tag is required.")
        if self.load_class not in LOAD_CLASSES:
            raise ValueError(f"Unsupported load class: {self.load_class!r}.")
        if not self.description.strip():
            raise ValueError("Load requirement description is required.")
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError("Load requirement quantity must be greater than zero.")
        if self.control_mode not in CONTROL_MODES:
            raise ValueError(f"Unsupported control mode: {self.control_mode!r}.")
        if self.drive_type not in DRIVE_TYPES:
            raise ValueError(f"Unsupported drive type: {self.drive_type!r}.")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        return asdict(self)


@dataclass(frozen=True)
class IORequirement:
    """The required behavior for one named I/O point tied to a load."""

    identity: str
    signal_identity: str
    signal_tag: str
    direction: str
    load_identity: str
    behavior: str
    fail_state: str = ""
    evidence_locator: str = ""

    def validate(self) -> None:
        if not self.identity.strip():
            raise ValueError("I/O requirement identity is required.")
        if not self.signal_identity.strip():
            raise ValueError("I/O requirement signal identity is required.")
        if not self.signal_tag.strip():
            raise ValueError("I/O requirement signal tag is required.")
        if self.direction not in IO_DIRECTIONS:
            raise ValueError(f"Unsupported I/O requirement direction: {self.direction!r}.")
        if not self.load_identity.strip():
            raise ValueError("I/O requirement must link to a load identity.")
        if not self.behavior.strip():
            raise ValueError("I/O requirement behavior is required.")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        return asdict(self)


@dataclass(frozen=True)
class HardwareRequirement:
    """A non-approved hardware class proposed from explicit resolver rules."""

    identity: str
    requirement_class: str
    quantity: int
    load_identity: str
    linked_io_identities: tuple[str, ...]
    evidence_locators: tuple[str, ...]
    unresolved_fields: tuple[str, ...]
    rationale: str
    rule_id: str
    status: str = RESOLUTION_NEEDS_ENGINEERING_DECISION

    def validate(self) -> None:
        if not self.identity.strip():
            raise ValueError("Hardware requirement identity is required.")
        if not self.requirement_class.strip():
            raise ValueError("Hardware requirement class is required.")
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError("Hardware requirement quantity must be greater than zero.")
        if not self.load_identity.strip():
            raise ValueError("Hardware requirement must link to a load identity.")
        if not self.rationale.strip() or not self.rule_id.strip():
            raise ValueError("Hardware requirement rationale and rule ID are required.")

    def to_dict(self) -> dict[str, object]:
        self.validate()
        payload = asdict(self)
        for name in ("linked_io_identities", "evidence_locators", "unresolved_fields"):
            payload[name] = list(payload[name])
        return payload


def serialize_load_requirement(requirement: LoadRequirement) -> str:
    return json.dumps(requirement.to_dict(), sort_keys=True, separators=(",", ":"))


def deserialize_load_requirement(record: str | dict[str, object]) -> LoadRequirement:
    payload = json.loads(record) if isinstance(record, str) else dict(record)
    requirement = LoadRequirement(
        identity=str(payload.get("identity", "")),
        tag=str(payload.get("tag", "")),
        load_class=str(payload.get("load_class", payload.get("loadClass", ""))),
        description=str(payload.get("description", "")),
        quantity=payload.get("quantity", 1),
        control_mode=str(payload.get("control_mode", payload.get("controlMode", "unknown"))),
        supply_voltage=str(payload.get("supply_voltage", payload.get("supplyVoltage", ""))),
        power=str(payload.get("power", "")),
        current=str(payload.get("current", "")),
        duty=str(payload.get("duty", "")),
        environment=str(payload.get("environment", "")),
        drive_type=str(payload.get("drive_type", payload.get("driveType", "unknown"))),
        evidence_locator=str(payload.get("evidence_locator", payload.get("evidenceLocator", ""))),
    )
    requirement.validate()
    return requirement


def serialize_io_requirement(requirement: IORequirement) -> str:
    return json.dumps(requirement.to_dict(), sort_keys=True, separators=(",", ":"))


def deserialize_io_requirement(record: str | dict[str, object]) -> IORequirement:
    payload = json.loads(record) if isinstance(record, str) else dict(record)
    requirement = IORequirement(
        identity=str(payload.get("identity", "")),
        signal_identity=str(payload.get("signal_identity", payload.get("signalIdentity", ""))),
        signal_tag=str(payload.get("signal_tag", payload.get("signalTag", ""))),
        direction=str(payload.get("direction", "")),
        load_identity=str(payload.get("load_identity", payload.get("loadIdentity", ""))),
        behavior=str(payload.get("behavior", "")),
        fail_state=str(payload.get("fail_state", payload.get("failState", ""))),
        evidence_locator=str(payload.get("evidence_locator", payload.get("evidenceLocator", ""))),
    )
    requirement.validate()
    return requirement


def serialize_hardware_requirement(requirement: HardwareRequirement) -> str:
    return json.dumps(requirement.to_dict(), sort_keys=True, separators=(",", ":"))


def load_requirements_from_project(project: object) -> tuple[LoadRequirement, ...]:
    return tuple(deserialize_load_requirement(record) for record in getattr(project, "LoadRequirements", []) or [])


def io_requirements_from_project(project: object) -> tuple[IORequirement, ...]:
    return tuple(deserialize_io_requirement(record) for record in getattr(project, "IORequirements", []) or [])


def persist_resolver_requirements(
    project: object,
    loads: tuple[LoadRequirement, ...],
    io_requirements: tuple[IORequirement, ...],
) -> tuple[HardwareRequirement, ...]:
    """Persist one validated resolver snapshot and return its proposed classes."""

    load_ids = set()
    for load in loads:
        load.validate()
        if load.identity in load_ids:
            raise ValueError(f"Duplicate load requirement identity: {load.identity!r}.")
        load_ids.add(load.identity)
    for requirement in io_requirements:
        requirement.validate()
        if requirement.load_identity not in load_ids:
            raise ValueError(f"I/O requirement {requirement.identity!r} links to an unknown load identity.")
    hardware = tuple(
        item
        for load in loads
        for item in resolve_hardware_classes(
            load,
            tuple(requirement for requirement in io_requirements if requirement.load_identity == load.identity),
        )
    )
    project.LoadRequirements = [serialize_load_requirement(load) for load in loads]
    project.IORequirements = [serialize_io_requirement(requirement) for requirement in io_requirements]
    project.HardwareRequirements = [serialize_hardware_requirement(requirement) for requirement in hardware]
    return hardware


def resolve_hardware_classes(load: LoadRequirement, io_requirements: tuple[IORequirement, ...] = ()) -> tuple[HardwareRequirement, ...]:
    """Return review-required generic hardware classes for one described load.

    The resolver is intentionally conservative.  It returns the hardware
    categories an engineer must resolve, rather than pretending to determine
    ratings, trip curves, SCCR, protection coordination, safety category, or
    a supplier part number from incomplete project intake.
    """

    load.validate()
    linked_io = tuple(io_requirements)
    for requirement in linked_io:
        requirement.validate()
        if requirement.load_identity != load.identity:
            raise ValueError(f"I/O requirement {requirement.identity!r} does not belong to load {load.identity!r}.")

    proposals: list[tuple[str, str, str]] = [
        ("branch_protection", "resolver.branch-protection.v1", "Every described controlled load requires an engineering review of branch protection."),
        ("disconnecting_means", "resolver.disconnect.v1", "Every described controlled load requires an engineering review of isolation/disconnecting means."),
    ]
    if load.load_class == "hydraulic":
        proposals.append(("hydraulic_power_interface", "resolver.hydraulic-interface.v1", "Hydraulic equipment requires an engineering review of its power interface; drive type is not inferred."))
    if load.load_class == "motor" or load.drive_type == "electric_motor":
        proposals.extend(
            [
                ("motor_switching", "resolver.motor-switching.v1", "Motor-driven load requires an engineering review of a contactor/starter or equivalent switching method."),
                ("motor_overload_protection", "resolver.motor-overload.v1", "Motor-driven load requires an engineering review of overload/motor protection."),
            ]
        )
    if load.control_mode == "speed_control":
        proposals.append(("variable_frequency_drive", "resolver.speed-control.v1", "Speed-control mode requires an engineering review of a VFD or equivalent drive."))
    if load.load_class == "robot":
        proposals.append(("robot_interface", "resolver.robot-interface.v1", "Robot load requires an engineering review of its control/power interface."))
    if any(requirement.direction in {"output", "analog_output"} for requirement in linked_io):
        proposals.append(("control_interface", "resolver.output-interface.v1", "An output requirement needs an engineering review of relay/interface/drive compatibility."))
    proposals.append(("terminal_connection", "resolver.terminal-connection.v1", "A controlled load requires an engineering review of terminal and field-connection requirements."))

    linked_io_identities = tuple(sorted(requirement.identity for requirement in linked_io))
    evidence_locators = tuple(sorted({value for value in (load.evidence_locator, *(item.evidence_locator for item in linked_io)) if value}))
    unresolved = _unresolved_fields(load, linked_io)
    return tuple(
        HardwareRequirement(
            identity=imported_ce_identity("controlforgecad.hardware-requirement", f"{load.identity}:{requirement_class}:{rule_id}"),
            requirement_class=requirement_class,
            quantity=load.quantity,
            load_identity=load.identity,
            linked_io_identities=linked_io_identities,
            evidence_locators=evidence_locators,
            unresolved_fields=unresolved,
            rationale=rationale,
            rule_id=rule_id,
        )
        for requirement_class, rule_id, rationale in proposals
    )


def _unresolved_fields(load: LoadRequirement, io_requirements: tuple[IORequirement, ...]) -> tuple[str, ...]:
    fields = []
    for name in ("supply_voltage", "power_or_current", "duty", "environment", "evidence_locator"):
        values = {
            "supply_voltage": load.supply_voltage,
            "power_or_current": load.power or load.current,
            "duty": load.duty,
            "environment": load.environment,
            "evidence_locator": load.evidence_locator,
        }
        if not values[name].strip():
            fields.append(name)
    if load.load_class == "hydraulic" and load.drive_type == "unknown":
        fields.append("drive_type")
    if any(not item.evidence_locator.strip() for item in io_requirements):
        fields.append("io_evidence_locator")
    return tuple(fields)
